import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Badge } from "./ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { 
  FileText,
  Plus,
  Calendar,
  User,
  Edit,
  Trash2,
  Eye,
  ChevronRight,
  ChevronDown,
  ExternalLink
} from "lucide-react";

const Policies = () => {
  const [policies, setPolicies] = useState([]);
  const [filteredPolicies, setFilteredPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  
  // Form state
  const [policyForm, setPolicyForm] = useState({
    title: "",
    content: "",
    category: "general",
    effective_date: "",
    version: "1.0"
  });
  const [selectedPolicy, setSelectedPolicy] = useState(null);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [showViewDialog, setShowViewDialog] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  const categories = [
    "general", "hr", "it", "security", "finance", "operations", "compliance", "health_safety"
  ];

  // Fetch policies
  useEffect(() => {
    fetchPolicies();
  }, []);

  // Apply filters
  useEffect(() => {
    let filtered = policies;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(policy =>
        policy.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        policy.content.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Category filter
    if (selectedCategory && selectedCategory !== "all") {
      filtered = filtered.filter(policy => policy.category === selectedCategory);
    }

    setFilteredPolicies(filtered);
  }, [policies, searchTerm, selectedCategory]);

  const fetchPolicies = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${backendUrl}/api/policies`);
      if (response.ok) {
        const data = await response.json();
        setPolicies(data);
      }
    } catch (error) {
      console.error('Error fetching policies:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePolicy = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/policies`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(policyForm),
      });

      if (response.ok) {
        setShowCreateDialog(false);
        setPolicyForm({
          title: "",
          content: "",
          category: "general",
          effective_date: "",
          version: "1.0"
        });
        fetchPolicies();
        alert('Policy created successfully!');
      } else {
        const error = await response.json();
        alert(`Error creating policy: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error creating policy:', error);
      alert('Failed to create policy');
    }
  };

  const handleUpdatePolicy = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/policies/${selectedPolicy.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(policyForm),
      });

      if (response.ok) {
        setShowEditDialog(false);
        setPolicyForm({
          title: "",
          content: "",
          category: "general",
          effective_date: "",
          version: "1.0"
        });
        setSelectedPolicy(null);
        fetchPolicies();
        alert('Policy updated successfully!');
      } else {
        const error = await response.json();
        alert(`Error updating policy: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error updating policy:', error);
      alert('Failed to update policy');
    }
  };

  const handleDeletePolicy = async (policyId) => {
    if (window.confirm('Are you sure you want to delete this policy?')) {
      try {
        const response = await fetch(`${backendUrl}/api/policies/${policyId}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          fetchPolicies();
          alert('Policy deleted successfully!');
        } else {
          alert('Failed to delete policy');
        }
      } catch (error) {
        console.error('Error deleting policy:', error);
        alert('Failed to delete policy');
      }
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not set';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short', 
      day: 'numeric'
    });
  };

  const getCategoryColor = (category) => {
    const colors = {
      general: 'bg-blue-100 text-blue-800',
      hr: 'bg-green-100 text-green-800',
      it: 'bg-purple-100 text-purple-800',
      security: 'bg-red-100 text-red-800',
      finance: 'bg-yellow-100 text-yellow-800',
      operations: 'bg-indigo-100 text-indigo-800',
      compliance: 'bg-orange-100 text-orange-800',
      health_safety: 'bg-pink-100 text-pink-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  const startEdit = (policy) => {
    setSelectedPolicy(policy);
    setPolicyForm({
      title: policy.title,
      content: policy.content,
      category: policy.category,
      effective_date: policy.effective_date ? new Date(policy.effective_date).toISOString().split('T')[0] : "",
      version: policy.version
    });
    setShowEditDialog(true);
  };

  const viewPolicy = (policy) => {
    setSelectedPolicy(policy);
    setShowViewDialog(true);
  };

  return (
    <div className="h-full flex flex-col space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Company Policies</h1>
        <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
          <DialogTrigger asChild>
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Plus className="h-4 w-4 mr-2" />
              Add Policy
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Create New Policy</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label>Title</Label>
                <Input
                  value={policyForm.title}
                  onChange={(e) => setPolicyForm(prev => ({ ...prev, title: e.target.value }))}
                  placeholder="Policy title..."
                />
              </div>
              
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label>Category</Label>
                  <Select value={policyForm.category} onValueChange={(value) => setPolicyForm(prev => ({ ...prev, category: value }))}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((cat) => (
                        <SelectItem key={cat} value={cat}>
                          {cat.replace('_', ' ').toUpperCase()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label>Version</Label>
                  <Input
                    value={policyForm.version}
                    onChange={(e) => setPolicyForm(prev => ({ ...prev, version: e.target.value }))}
                    placeholder="1.0"
                  />
                </div>
                
                <div>
                  <Label>Effective Date</Label>
                  <Input
                    type="date"
                    value={policyForm.effective_date}
                    onChange={(e) => setPolicyForm(prev => ({ ...prev, effective_date: e.target.value }))}
                  />
                </div>
              </div>
              
              <div>
                <Label>Content</Label>
                <Textarea
                  value={policyForm.content}
                  onChange={(e) => setPolicyForm(prev => ({ ...prev, content: e.target.value }))}
                  placeholder="Policy content..."
                  rows={8}
                />
              </div>
              
              <div className="flex gap-2">
                <Button onClick={handleCreatePolicy} disabled={!policyForm.title || !policyForm.content}>
                  Create Policy
                </Button>
                <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
                  Cancel
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filters & Search
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="relative md:col-span-2">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search policies..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger>
                <SelectValue placeholder="Select Category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {categories.map((cat) => (
                  <SelectItem key={cat} value={cat}>
                    {cat.replace('_', ' ').toUpperCase()}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Policies List */}
      <div className="flex-1 overflow-auto">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-gray-500">Loading policies...</div>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredPolicies.map((policy) => (
              <Card key={policy.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="text-lg">{policy.title}</CardTitle>
                      <div className="flex items-center gap-4 text-sm text-gray-500 mt-2">
                        <Badge className={`${getCategoryColor(policy.category)} border-0`}>
                          {policy.category.replace('_', ' ').toUpperCase()}
                        </Badge>
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          Effective: {formatDate(policy.effective_date)}
                        </div>
                        <div className="flex items-center gap-1">
                          <FileText className="h-4 w-4" />
                          Version {policy.version}
                        </div>
                        <div className="flex items-center gap-1">
                          <User className="h-4 w-4" />
                          {policy.author}
                        </div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" onClick={() => viewPolicy(policy)}>
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button size="sm" variant="outline" onClick={() => startEdit(policy)}>
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button size="sm" variant="outline" onClick={() => handleDeletePolicy(policy.id)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 line-clamp-3">
                    {policy.content.substring(0, 200)}...
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {!loading && filteredPolicies.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg">No policies found</div>
            <div className="text-gray-400 text-sm mt-2">Try adjusting your filters or create a new policy</div>
          </div>
        )}
      </div>

      {/* Edit Dialog */}
      <Dialog open={showEditDialog} onOpenChange={setShowEditDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Edit Policy</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label>Title</Label>
              <Input
                value={policyForm.title}
                onChange={(e) => setPolicyForm(prev => ({ ...prev, title: e.target.value }))}
                placeholder="Policy title..."
              />
            </div>
            
            <div className="grid grid-cols-3 gap-4">
              <div>
                <Label>Category</Label>
                <Select value={policyForm.category} onValueChange={(value) => setPolicyForm(prev => ({ ...prev, category: value }))}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((cat) => (
                      <SelectItem key={cat} value={cat}>
                        {cat.replace('_', ' ').toUpperCase()}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label>Version</Label>
                <Input
                  value={policyForm.version}
                  onChange={(e) => setPolicyForm(prev => ({ ...prev, version: e.target.value }))}
                  placeholder="1.0"
                />
              </div>
              
              <div>
                <Label>Effective Date</Label>
                <Input
                  type="date"
                  value={policyForm.effective_date}
                  onChange={(e) => setPolicyForm(prev => ({ ...prev, effective_date: e.target.value }))}
                />
              </div>
            </div>
            
            <div>
              <Label>Content</Label>
              <Textarea
                value={policyForm.content}
                onChange={(e) => setPolicyForm(prev => ({ ...prev, content: e.target.value }))}
                placeholder="Policy content..."
                rows={8}
              />
            </div>
            
            <div className="flex gap-2">
              <Button onClick={handleUpdatePolicy} disabled={!policyForm.title || !policyForm.content}>
                Update Policy
              </Button>
              <Button variant="outline" onClick={() => setShowEditDialog(false)}>
                Cancel
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* View Dialog */}
      <Dialog open={showViewDialog} onOpenChange={setShowViewDialog}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>{selectedPolicy?.title}</DialogTitle>
          </DialogHeader>
          {selectedPolicy && (
            <div className="space-y-4">
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <Badge className={`${getCategoryColor(selectedPolicy.category)} border-0`}>
                  {selectedPolicy.category.replace('_', ' ').toUpperCase()}
                </Badge>
                <div className="flex items-center gap-1">
                  <Calendar className="h-4 w-4" />
                  Effective: {formatDate(selectedPolicy.effective_date)}
                </div>
                <div className="flex items-center gap-1">
                  <FileText className="h-4 w-4" />
                  Version {selectedPolicy.version}
                </div>
                <div className="flex items-center gap-1">
                  <User className="h-4 w-4" />
                  {selectedPolicy.author}
                </div>
              </div>
              <div className="prose max-w-none">
                <pre className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                  {selectedPolicy.content}
                </pre>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Policies;