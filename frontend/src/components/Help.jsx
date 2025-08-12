import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Textarea } from './ui/textarea';
import { Input } from './ui/input';
import { PlusCircle, MessageSquare, Calendar, User, Reply, Trash2, CheckCircle, Clock } from 'lucide-react';
import { toast } from 'sonner';

const Help = () => {
  const [messages, setMessages] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [replyingTo, setReplyingTo] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    message: '',
    priority: 'normal'
  });
  const [replyData, setReplyData] = useState({
    message: ''
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/help`);
      if (response.ok) {
        const data = await response.json();
        setMessages(data);
        console.log(`Loaded ${data.length} help requests from backend`);
      } else {
        throw new Error('Failed to fetch help messages');
      }
    } catch (error) {
      console.error('Error fetching help messages:', error);
      toast.error('Failed to load help messages. Please try again.');
      
      // Retry mechanism
      setTimeout(() => {
        console.log('Retrying to fetch help messages...');
        fetchMessages();
      }, 3000);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    
    try {
      // Show saving indicator
      toast.info('Saving your help request...', { duration: 1000 });
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/help`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const savedRequest = await response.json();
        
        // Verify the request was saved by fetching it back
        const verifyResponse = await fetch(`${import.meta.env.REACT_APP_BACKEND_URL}/api/help`);
        const allRequests = await verifyResponse.json();
        const wasSaved = allRequests.find(req => req.id === savedRequest.id);
        
        if (wasSaved) {
          toast.success(`Help request saved successfully! Request ID: ${savedRequest.id}`);
          console.log('✅ Request verified as saved:', savedRequest.id);
        } else {
          toast.warning('Request submitted but verification failed. Please refresh to check.');
        }
        
        setFormData({ title: '', message: '', priority: 'normal' });
        setShowAddForm(false);
        fetchMessages();
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to submit help request');
      }
    } catch (error) {
      console.error('Error submitting help request:', error);
      toast.error(`Failed to submit help request: ${error.message}`);
      
      // Don't clear form data on error so user doesn't lose their work
      console.log('Form data preserved due to error');
    } finally {
      setSaving(false);
    }
  };

  const handleReply = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${import.meta.env.REACT_APP_BACKEND_URL}/api/help/${replyingTo.id}/reply`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(replyData),
      });

      if (response.ok) {
        toast.success('Reply sent successfully');
        setReplyData({ message: '' });
        setReplyingTo(null);
        fetchMessages();
      } else {
        throw new Error('Failed to send reply');
      }
    } catch (error) {
      console.error('Error sending reply:', error);
      toast.error('Failed to send reply');
    }
  };

  const handleStatusUpdate = async (messageId, newStatus) => {
    try {
      const response = await fetch(`${import.meta.env.REACT_APP_BACKEND_URL}/api/help/${messageId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });

      if (response.ok) {
        toast.success('Status updated successfully');
        fetchMessages();
      } else {
        throw new Error('Failed to update status');
      }
    } catch (error) {
      console.error('Error updating status:', error);
      toast.error('Failed to update status');
    }
  };

  const handleDelete = async (messageId) => {
    if (!confirm('Are you sure you want to delete this help request?')) return;
    
    try {
      const response = await fetch(`${import.meta.env.REACT_APP_BACKEND_URL}/api/help/${messageId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        toast.success('Help request deleted successfully');
        fetchMessages();
      } else {
        throw new Error('Failed to delete help request');
      }
    } catch (error) {
      console.error('Error deleting help request:', error);
      toast.error('Failed to delete help request');
    }
  };

  const handleClearResolved = async () => {
    const resolvedMessages = messages.filter(msg => msg.status === 'resolved');
    if (resolvedMessages.length === 0) {
      toast.info('No resolved requests to clear');
      return;
    }

    if (!confirm(`Are you sure you want to delete all ${resolvedMessages.length} resolved help requests? This action cannot be undone.`)) {
      return;
    }

    try {
      setLoading(true);
      const deletePromises = resolvedMessages.map(msg => 
        fetch(`${import.meta.env.REACT_APP_BACKEND_URL}/api/help/${msg.id}`, {
          method: 'DELETE',
        })
      );

      const responses = await Promise.all(deletePromises);
      const successful = responses.filter(response => response.ok).length;
      const failed = responses.length - successful;

      if (successful > 0) {
        toast.success(`Successfully cleared ${successful} resolved requests${failed > 0 ? ` (${failed} failed)` : ''}`);
        fetchMessages();
      } else {
        toast.error('Failed to clear resolved requests');
      }
    } catch (error) {
      console.error('Error clearing resolved requests:', error);
      toast.error('Failed to clear resolved requests');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'resolved': return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'in_progress': return <Clock className="h-4 w-4 text-yellow-600" />;
      default: return <MessageSquare className="h-4 w-4 text-blue-600" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'resolved': return 'bg-green-100 text-green-800';
      case 'in_progress': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-blue-100 text-blue-800';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-blue-100 text-blue-800';
    }
  };

  const filteredMessages = messages.filter(message => {
    if (filter === 'all') return true;
    return message.status === filter;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-blue-600">Loading help requests...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Status Info */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-blue-900">Help & Support</h2>
          <div className="flex items-center gap-4 mt-1">
            <p className="text-blue-600">Submit support requests and track their progress</p>
            {messages.length > 0 && (
              <div className="text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
                {messages.length} total requests • {messages.filter(m => m.status === 'open').length} open • {messages.filter(m => m.status === 'resolved').length} resolved
              </div>
            )}
          </div>
        </div>
        <Button
          onClick={() => {
            setShowAddForm(!showAddForm);
            setReplyingTo(null);
            setFormData({ title: '', message: '', priority: 'normal' });
          }}
          className="bg-blue-600 hover:bg-blue-700 text-white"
          disabled={loading}
        >
          <PlusCircle className="h-4 w-4 mr-2" />
          New Request
        </Button>
      </div>

      {/* Filter Buttons */}
      <div className="flex gap-2 flex-wrap justify-between items-center">
        <div className="flex gap-2 flex-wrap">
          {['all', 'open', 'in_progress', 'resolved'].map((status) => (
            <Button
              key={status}
              onClick={() => setFilter(status)}
              variant={filter === status ? "default" : "outline"}
              size="sm"
              className={filter === status ? "bg-blue-600 hover:bg-blue-700" : ""}
            >
              {status === 'all' ? 'All Requests' : status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </Button>
          ))}
        </div>
        
        {/* Clear Resolved Button */}
        {messages.filter(msg => msg.status === 'resolved').length > 0 && (
          <Button
            onClick={handleClearResolved}
            variant="outline"
            size="sm"
            className="text-red-600 border-red-300 hover:bg-red-50 hover:border-red-400"
            disabled={loading}
          >
            <Trash2 className="h-4 w-4 mr-2" />
            Clear All Resolved ({messages.filter(msg => msg.status === 'resolved').length})
          </Button>
        )}
      </div>

      {/* Add Form */}
      {showAddForm && (
        <Card className="border-blue-200 shadow-sm">
          <CardHeader className="bg-blue-50">
            <CardTitle className="text-blue-900">Submit New Help Request</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-blue-900 mb-2">Subject</label>
                  <Input
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    placeholder="Brief description of your issue"
                    required
                    className="border-blue-200 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-blue-900 mb-2">Priority</label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    className="w-full p-2 border border-blue-200 rounded-md focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="normal">Normal</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-blue-900 mb-2">Message</label>
                <Textarea
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  placeholder="Please provide detailed information about your issue or request"
                  required
                  rows={4}
                  className="border-blue-200 focus:border-blue-500"
                />
              </div>
              <div className="flex gap-2">
                <Button 
                  type="submit" 
                  className="bg-blue-600 hover:bg-blue-700"
                  disabled={saving}
                >
                  {saving ? (
                    <>
                      <Clock className="h-4 w-4 mr-2 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    'Submit Request'
                  )}
                </Button>
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => {
                    setShowAddForm(false);
                    setFormData({ title: '', message: '', priority: 'normal' });
                  }}
                  disabled={saving}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Reply Form */}
      {replyingTo && (
        <Card className="border-green-200 shadow-sm">
          <CardHeader className="bg-green-50">
            <CardTitle className="text-green-900">Reply to: {replyingTo.title}</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <form onSubmit={handleReply} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-green-900 mb-2">Your Reply</label>
                <Textarea
                  value={replyData.message}
                  onChange={(e) => setReplyData({ ...replyData, message: e.target.value })}
                  placeholder="Type your reply here..."
                  required
                  rows={3}
                  className="border-green-200 focus:border-green-500"
                />
              </div>
              <div className="flex gap-2">
                <Button type="submit" className="bg-green-600 hover:bg-green-700 text-white">
                  Send Reply
                </Button>
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => {
                    setReplyingTo(null);
                    setReplyData({ message: '' });
                  }}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Messages List */}
      <div className="space-y-4">
        {filteredMessages.length === 0 ? (
          <Card className="border-blue-200">
            <CardContent className="p-8 text-center">
              <MessageSquare className="h-12 w-12 text-blue-400 mx-auto mb-4" />
              <div className="text-blue-600 mb-2">No help requests found</div>
              <p className="text-sm text-gray-600">
                {filter === 'all' ? 'Click "New Request" to submit your first help request.' : `No ${filter.replace('_', ' ')} requests found.`}
              </p>
            </CardContent>
          </Card>
        ) : (
          filteredMessages.map((message) => (
            <Card key={message.id} className="border-blue-200 shadow-sm hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="text-lg font-semibold text-blue-900">{message.title}</h3>
                      <div className="flex gap-2">
                        <Badge className={`text-xs ${getStatusColor(message.status)}`}>
                          {getStatusIcon(message.status)}
                          <span className="ml-1">{message.status.replace('_', ' ').toUpperCase()}</span>
                        </Badge>
                        <Badge className={`text-xs ${getPriorityColor(message.priority)}`}>
                          {message.priority.toUpperCase()}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-blue-600 mb-3">
                      <div className="flex items-center gap-1">
                        <User className="h-4 w-4" />
                        {message.author || 'Anonymous'}
                      </div>
                      <div className="flex items-center gap-1">
                        <Calendar className="h-4 w-4" />
                        {new Date(message.created_at).toLocaleDateString()}
                      </div>
                      {message.replies && message.replies.length > 0 && (
                        <div className="flex items-center gap-1">
                          <Reply className="h-4 w-4" />
                          {message.replies.length} replies
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setReplyingTo(message)}
                      className="text-green-600 hover:bg-green-50"
                    >
                      <Reply className="h-4 w-4" />
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDelete(message.id)}
                      className="text-red-600 hover:bg-red-50"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <p className="text-gray-700 leading-relaxed">{message.message}</p>
                </div>

                {/* Status Update Buttons */}
                {message.status !== 'resolved' && (
                  <div className="flex gap-2 mb-4 pb-4 border-b border-gray-200">
                    {message.status === 'open' && (
                      <Button
                        size="sm"
                        onClick={() => handleStatusUpdate(message.id, 'in_progress')}
                        className="bg-yellow-600 hover:bg-yellow-700 text-white"
                      >
                        Mark In Progress
                      </Button>
                    )}
                    <Button
                      size="sm"
                      onClick={() => handleStatusUpdate(message.id, 'resolved')}
                      className="bg-green-600 hover:bg-green-700 text-white"
                    >
                      Mark Resolved
                    </Button>
                  </div>
                )}

                {/* Replies */}
                {message.replies && message.replies.length > 0 && (
                  <div className="space-y-3">
                    <h4 className="font-medium text-blue-900">Replies:</h4>
                    {message.replies.map((reply, index) => (
                      <div key={index} className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-200">
                        <div className="flex items-center gap-2 mb-2 text-sm text-blue-600">
                          <User className="h-4 w-4" />
                          <span>{reply.author || 'Administrator'}</span>
                          <Calendar className="h-4 w-4" />
                          <span>{new Date(reply.created_at).toLocaleDateString()}</span>
                        </div>
                        <p className="text-gray-700">{reply.message}</p>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default Help;