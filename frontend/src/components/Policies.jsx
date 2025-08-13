import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "./ui/dialog";
import { 
  FileText,
  Calendar,
  User,
  ChevronRight,
  ChevronDown,
  ExternalLink
} from "lucide-react";

const Policies = () => {
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedSections, setExpandedSections] = useState({
    hr: true,
    it: false,
    admin: false,
    other: false
  });
  
  const [selectedPolicy, setSelectedPolicy] = useState(null);
  const [showViewDialog, setShowViewDialog] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  // Policy structure data
  const policyStructure = {
    hr: {
      title: "HR POLICY",
      policies: [
        { title: "Employee Code of Conduct", link: "#", description: "Guidelines for professional behavior and workplace ethics" },
        { title: "Leave and Attendance Policy", link: "#", description: "Rules for time off requests and attendance requirements" },
        { title: "Performance Management", link: "#", description: "Performance evaluation and improvement processes" },
        { title: "Grievance Procedure", link: "#", description: "Process for reporting and resolving workplace issues" },
        { title: "Anti-Harassment Policy", link: "#", description: "Zero tolerance policy for workplace harassment" }
      ]
    },
    it: {
      title: "IT POLICY",
      policies: [
        { title: "Data Security Guidelines", link: "#", description: "Best practices for protecting company data" },
        { title: "System Access Control", link: "#", description: "Rules for system login and access permissions" },
        { title: "Software Usage Policy", link: "#", description: "Approved software and licensing guidelines" },
        { title: "Email and Communication", link: "#", description: "Professional email usage and communication standards" },
        { title: "Device Management", link: "#", description: "Company device usage and security requirements" }
      ]
    },
    admin: {
      title: "ADMIN POLICY",
      policies: [
        { title: "Office Space Management", link: "#", description: "Guidelines for workspace allocation and usage" },
        { title: "Expense Reimbursement", link: "#", description: "Process for business expense claims and approvals" },
        { title: "Travel Policy", link: "#", description: "Business travel guidelines and procedures" },
        { title: "Vendor Management", link: "#", description: "Procurement and vendor relationship guidelines" },
        { title: "Document Management", link: "#", description: "File storage, retention, and organization standards" }
      ]
    },
    other: {
      title: "OTHER POLICIES",
      policies: [
        { title: "Health and Safety", link: "#", description: "Workplace safety standards and emergency procedures" },
        { title: "Environmental Policy", link: "#", description: "Company commitment to environmental responsibility" },
        { title: "Quality Assurance", link: "#", description: "Standards for maintaining product and service quality" },
        { title: "Compliance Framework", link: "#", description: "Regulatory compliance and audit procedures" },
        { title: "Business Continuity", link: "#", description: "Plans for maintaining operations during disruptions" }
      ]
    }
  };

  // Fetch policies
  useEffect(() => {
    fetchPolicies();
  }, []);

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

  const formatDate = (dateString) => {
    if (!dateString) return 'Not set';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short', 
      day: 'numeric'
    });
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const viewPolicy = (policy) => {
    setSelectedPolicy(policy);
    setShowViewDialog(true);
  };

  return (
    <div className="h-full flex flex-col space-y-6">
      {/* Banner Image */}
      <div 
        className="relative h-48 bg-cover bg-center rounded-lg overflow-hidden"
        style={{
          backgroundImage: `url('https://images.pexels.com/photos/5816299/pexels-photo-5816299.jpeg')`,
        }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="text-center text-white">
            <h1 className="text-4xl font-bold mb-2">Company Policies</h1>
            <p className="text-lg opacity-90">Governance, Compliance & Professional Standards</p>
          </div>
        </div>
      </div>

      <div className="flex-1">
        {/* Policy Tree Structure - Full Width */}
        <div className="w-full space-y-4">
          {Object.entries(policyStructure).map(([key, section]) => (
            <Card key={key} className="overflow-visible">
              <CardHeader 
                className="cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => toggleSection(key)}
              >
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg font-bold text-gray-800">
                    {section.title}
                  </CardTitle>
                  {expandedSections[key] ? (
                    <ChevronDown className="h-5 w-5 text-gray-600" />
                  ) : (
                    <ChevronRight className="h-5 w-5 text-gray-600" />
                  )}
                </div>
              </CardHeader>
              
              {expandedSections[key] && (
                <CardContent className="pt-0 relative overflow-visible">
                  <div className="space-y-2">
                    {section.policies.map((policy, index) => (
                      <div 
                        key={index}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-md hover:bg-gray-100 transition-all duration-300 transform animate-in slide-in-from-left-4 fade-in"
                        style={{ 
                          animationDelay: `${index * 50}ms`,
                          animationFillMode: 'both'
                        }}
                      >
                        <div className="flex-1">
                          <div className="font-medium text-gray-800 mb-1">
                            {policy.title}
                          </div>
                          <div className="text-xs text-gray-500">
                            {policy.description}
                          </div>
                        </div>
                        <Button
                          size="sm"
                          variant="ghost"
                          className="text-blue-600 hover:text-blue-800 ml-2 transform hover:scale-105 transition-transform"
                        >
                          <ExternalLink className="h-4 w-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              )}
            </Card>
          ))}
        </div>

        {/* Policy Management - Right Side */}
        <div className="w-2/3 space-y-4">
          {/* Header */}
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold text-gray-900">Policy Management</h2>
          </div>

          {/* Existing Policies List */}
          <div className="flex-1 overflow-auto">
            {loading ? (
              <div className="flex justify-center items-center h-64">
                <div className="text-gray-500">Loading policies...</div>
              </div>
            ) : (
              <div className="space-y-3">
                {policies.map((policy) => (
                  <Card key={policy.id} className="hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="font-medium text-gray-800 mb-1">{policy.title}</h3>
                          <div className="flex items-center gap-3 text-xs text-gray-500 mb-2">
                            <Badge className={`
                              ${policy.category === 'hr' ? 'bg-green-100 text-green-800' : ''}
                              ${policy.category === 'it' ? 'bg-purple-100 text-purple-800' : ''}
                              ${policy.category === 'admin' ? 'bg-blue-100 text-blue-800' : ''}
                              ${policy.category === 'other' ? 'bg-gray-100 text-gray-800' : ''}
                              border-0
                            `}>
                              {policy.category.toUpperCase()}
                            </Badge>
                            <span className="flex items-center gap-1">
                              <Calendar className="h-3 w-3" />
                              {formatDate(policy.effective_date)}
                            </span>
                            <span className="flex items-center gap-1">
                              <FileText className="h-3 w-3" />
                              v{policy.version}
                            </span>
                          </div>
                          <p className="text-gray-600 text-sm line-clamp-2">
                            {policy.content.substring(0, 120)}...
                          </p>
                        </div>
                        <div className="flex gap-1 ml-4">
                          <Button size="sm" variant="ghost" onClick={() => viewPolicy(policy)}>
                            View Policy
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
                
                {policies.length === 0 && (
                  <div className="text-center py-8">
                    <div className="text-gray-400 text-base">Policy documents will be displayed here when available</div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* View Dialog */}
      <Dialog open={showViewDialog} onOpenChange={setShowViewDialog}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>{selectedPolicy?.title}</DialogTitle>
          </DialogHeader>
          {selectedPolicy && (
            <div className="space-y-4">
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <Badge className={`
                  ${selectedPolicy.category === 'hr' ? 'bg-green-100 text-green-800' : ''}
                  ${selectedPolicy.category === 'it' ? 'bg-purple-100 text-purple-800' : ''}
                  ${selectedPolicy.category === 'admin' ? 'bg-blue-100 text-blue-800' : ''}
                  ${selectedPolicy.category === 'other' ? 'bg-gray-100 text-gray-800' : ''}
                  border-0
                `}>
                  {selectedPolicy.category.toUpperCase()}
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