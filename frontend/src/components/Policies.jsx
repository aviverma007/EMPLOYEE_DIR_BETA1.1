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

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Policy structure data based on actual company policy files
  const policyStructure = {
    hr: {
      title: "HR POLICY",
      policies: [
        { 
          title: "Leave Policy", 
          link: "/company policies/_14_33_50e319284d7e4fe4_Leave Policy (Revised).pdf", 
          description: "Comprehensive leave policy including annual, sick, and special leaves" 
        },
        { 
          title: "Employee Referral Program", 
          link: "/company policies/_14_19_2fe9bd4b1c514d00_Employee referral policy.pdf", 
          description: "Guidelines for employee referral bonus and procedures" 
        },
        { 
          title: "Sexual Harassment Prevention", 
          link: "/company policies/_12_39_b356500c83384d2d_Sexual Harassment At Work Redressal Policy_26-Apr-22.pdf", 
          description: "Zero tolerance policy and redressal mechanism for workplace harassment" 
        },
        { 
          title: "Dress Code Guidelines", 
          link: "/company policies/_13_55_00673d13502c42da_Dress code policy.pdf", 
          description: "Professional dress code standards for workplace appearance" 
        }
      ]
    },
    attendance: {
      title: "ATTENDANCE POLICY",
      policies: [
        { 
          title: "Business Hours Attendance", 
          link: "/company policies/_11_11_70bde4e9a0a04aed_Business Hours Attendance Policy.pdf", 
          description: "Working hours, timings, and attendance tracking procedures" 
        },
        { 
          title: "Revised Attendance Policy 2025", 
          link: "/company policies/_36_12_f19af68b04f849ee_Revised Attendance Policy w.e.f 21st May 25.pdf", 
          description: "Updated attendance rules effective from May 21st, 2025" 
        },
        { 
          title: "Flexible Work Schedule", 
          link: "/company policies/Microsoft Word - Flexible Work Schedule.pdf", 
          description: "Guidelines for flexible working hours and remote work options" 
        }
      ]
    },
    finance: {
      title: "FINANCE POLICY",
      policies: [
        { 
          title: "Local Conveyance Policy", 
          link: "/company policies/_15_9_02985794b8584650_Local Conveyance policy.pdf", 
          description: "Reimbursement guidelines for local travel and transportation" 
        },
        { 
          title: "Tour & Travel Policy", 
          link: "/company policies/_23_44_6eca6e909cee4aa7_Tour Travel Policy.pdf", 
          description: "Business travel expenses, booking procedures, and reimbursements" 
        },
        { 
          title: "Night Shift Meal Allowance", 
          link: "/company policies/_38_0_62d66a9aaaf645cc_Meal and Conveyance for Employees Working at Night on Sites.pdf", 
          description: "Meal and conveyance allowance for employees working night shifts on sites" 
        }
      ]
    },
    governance: {
      title: "GOVERNANCE POLICY",
      policies: [
        { 
          title: "Whistle Blower Policy", 
          link: "/company policies/_16_4_3edd02c8f36f429f_Whistle Blower Policy.pdf", 
          description: "Protected reporting mechanism for unethical practices and violations" 
        }
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