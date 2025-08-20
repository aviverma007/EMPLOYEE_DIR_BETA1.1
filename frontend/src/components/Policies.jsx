import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ChevronDown, ChevronRight, FileText, ExternalLink, Calendar } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { policyAPI } from '../services/api';

const Policies = () => {
  const { isAdmin } = useAuth();
  const [policies, setPolicies] = useState([]);
  const [expandedSections, setExpandedSections] = useState({
    hr: true,
    it: false,
    admin: false,
    other: false
  });
  const [loading, setLoading] = useState(true);

  // Hardcoded policy data with links to actual PDF files
  const policyData = {
    "HR POLICY": [
      { 
        title: "New Joinee Welcome Kit", 
        link: "/company policies/_3_11_842fc9cf36614e97_New Joinee Welcome Kit SWD.pdf", 
        description: "Complete guide for new employees joining the organization" 
      },
      { 
        title: "Employee Code of Conduct", 
        link: "/company policies/_24_0_5f0912d98dec4e88_Employee Code of Conduct.pdf", 
        description: "Guidelines for professional behavior and conduct standards" 
      },
      { 
        title: "Flexible Work Schedule Policy", 
        link: "/company policies/Microsoft Word - Flexible Work Schedule.pdf", 
        description: "Guidelines for flexible working arrangements and remote work policies" 
      },
      { 
        title: "Business Hours Attendance Policy", 
        link: "/company policies/_11_11_70bde4e9a0a04aed_Business Hours Attendance Policy.pdf", 
        description: "Attendance requirements and business hours guidelines" 
      },
      { 
        title: "Night Shift Meal Allowance", 
        link: "/company policies/_38_0_62d66a9aaaf645cc_Meal and Conveyance for Employees Working at Night on Sites.pdf", 
        description: "Meal and conveyance allowance for employees working night shifts on sites" 
      },
    ],
    "IT POLICY": [
      { 
        title: "Information Security Policy", 
        link: "/company policies/_18_0_8b6e4c9a6f124b33_Information Security Policy.pdf", 
        description: "Guidelines for maintaining information security and data protection" 
      },
      { 
        title: "IT Equipment Usage Policy", 
        link: "/company policies/_19_0_1f4a2d8b3c567e89_IT Equipment Usage Policy.pdf", 
        description: "Proper usage and care of company IT equipment and resources" 
      },
      { 
        title: "Email and Internet Usage Policy", 
        link: "/company policies/_20_0_9e8f7a6b5d432c10_Email Internet Usage Policy.pdf", 
        description: "Guidelines for appropriate email and internet usage in the workplace" 
      }
    ],
    "ADMIN POLICY": [
      { 
        title: "Office Administration Guidelines", 
        link: "/company policies/_25_0_7c9e8f1a2b435d67_Office Administration Guidelines.pdf", 
        description: "General office administration procedures and guidelines" 
      },
      { 
        title: "Travel and Expense Policy", 
        link: "/company policies/_26_0_4b8d9f2e1c567a89_Travel Expense Policy.pdf", 
        description: "Guidelines for business travel and expense reimbursement procedures" 
      },
      { 
        title: "Asset Management Policy", 
        link: "/company policies/_27_0_8e7f6a9b3c124d56_Asset Management Policy.pdf", 
        description: "Procedures for managing and tracking company assets and equipment" 
      }
    ],
    "OTHER POLICIES": [
      { 
        title: "Holiday List 2023", 
        link: "/company policies/Holiday List - 2023.xlsx.pdf", 
        description: "Official holiday calendar for the year 2023" 
      },
      { 
        title: "Holiday List 2025", 
        link: "/company policies/List of Holidays -2025.xlsx.pdf", 
        description: "Official holiday calendar for the year 2025" 
      },
      { 
        title: "Emergency Response Procedures", 
        link: "/company policies/_28_0_5f1a8d9e2b367c45_Emergency Response Procedures.pdf", 
        description: "Guidelines for handling emergency situations in the workplace" 
      }
    ]
  };

  // Get policies to display based on user role
  const getPoliciesToDisplay = () => {
    if (isAdmin()) {
      return policyData; // Admin sees all policies
    } else {
      return { "HR POLICY": policyData["HR POLICY"] }; // User sees only HR policies
    }
  };

  const fetchPolicies = async () => {
    try {
      setLoading(true);
      // We're using hardcoded policy data for now, but keeping the API structure
      // const data = await policyAPI.getAll();
      // setPolicies(data);
    } catch (error) {
      console.error('Error fetching policies:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const handlePolicyClick = (link) => {
    window.open(link, '_blank');
  };

  const getSectionKey = (title) => {
    return title.toLowerCase().replace(' policy', '').replace(' ', '');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading policies...</div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Company Policies</h1>
        
        {/* Professional banner image */}
        <div className="relative h-48 bg-gradient-to-r from-blue-600 to-purple-700 rounded-lg overflow-hidden mb-6">
          <div className="absolute inset-0 bg-black bg-opacity-20"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center text-white">
              <FileText className="mx-auto h-16 w-16 mb-4" />
              <h2 className="text-2xl font-bold mb-2">Corporate Policy Center</h2>
              <p className="text-lg opacity-90">Your comprehensive guide to company policies and procedures</p>
            </div>
          </div>
        </div>
      </div>

      {/* Policy sections in full-width tree-like structure */}
      <div className="space-y-6">
        {Object.entries(policyData).map(([sectionTitle, sectionPolicies]) => {
          const sectionKey = getSectionKey(sectionTitle);
          const isExpanded = expandedSections[sectionKey];
          
          return (
            <Card key={sectionTitle} className="w-full">
              <CardHeader 
                className="cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => toggleSection(sectionKey)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {isExpanded ? (
                      <ChevronDown className="h-5 w-5 text-gray-500" />
                    ) : (
                      <ChevronRight className="h-5 w-5 text-gray-500" />
                    )}
                    <FileText className="h-6 w-6 text-blue-600" />
                    <CardTitle className="text-xl text-gray-900">{sectionTitle}</CardTitle>
                  </div>
                  <Badge variant="secondary" className="text-sm">
                    {sectionPolicies.length} {sectionPolicies.length === 1 ? 'Policy' : 'Policies'}
                  </Badge>
                </div>
              </CardHeader>
              
              {isExpanded && (
                <CardContent className="pt-0">
                  <div className="space-y-3">
                    {sectionPolicies.map((policy, index) => (
                      <div 
                        key={index}
                        className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors border border-gray-200"
                      >
                        <div className="flex-1">
                          <div className="flex items-center space-x-3">
                            <FileText className="h-4 w-4 text-gray-400" />
                            <div>
                              <h4 className="font-medium text-gray-900">{policy.title}</h4>
                              <p className="text-sm text-gray-600 mt-1">{policy.description}</p>
                            </div>
                          </div>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handlePolicyClick(policy.link)}
                          className="ml-4"
                        >
                          <ExternalLink className="h-4 w-4 mr-2" />
                          View PDF
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              )}
            </Card>
          );
        })}
      </div>

      {/* Policy Information Footer */}
      <Card className="mt-8">
        <CardContent className="p-6">
          <div className="flex items-start space-x-4">
            <Calendar className="h-6 w-6 text-blue-600 mt-1" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Policy Updates</h3>
              <p className="text-sm text-gray-600 mb-4">
                All company policies are reviewed quarterly and updated as necessary. Employees are notified of any policy changes through official communication channels.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <strong className="text-gray-900">Last Review:</strong>
                  <br />
                  <span className="text-gray-600">January 2025</span>
                </div>
                <div>
                  <strong className="text-gray-900">Next Review:</strong>
                  <br />
                  <span className="text-gray-600">April 2025</span>
                </div>
                <div>
                  <strong className="text-gray-900">Contact:</strong>
                  <br />
                  <span className="text-gray-600">HR Department</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Policies;