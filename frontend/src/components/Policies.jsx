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
    hr: true
  });
  const [loading, setLoading] = useState(true);

  // All policies under single HR POLICY heading - mapped to actual files
  const policyData = {
    "HR POLICY": [
      { 
        title: "Business Hours Attendance Policy", 
        link: "/company policies/_11_11_70bde4e9a0a04aed_Business Hours Attendance Policy.pdf", 
        description: "Attendance requirements and business hours guidelines"
      },
      { 
        title: "Sexual Harassment At Work Redressal Policy", 
        link: "/company policies/_12_39_b356500c83384d2d_Sexual Harassment At Work Redressal Policy_26-Apr-22.pdf", 
        description: "Workplace harassment prevention and redressal procedures"
      },
      { 
        title: "Dress Code Policy", 
        link: "/company policies/_13_55_00673d13502c42da_Dress code policy.pdf", 
        description: "Professional dress code guidelines and standards"
      },
      { 
        title: "Employee Referral Policy", 
        link: "/company policies/_14_19_2fe9bd4b1c514d00_Employee referral policy.pdf", 
        description: "Employee referral program guidelines and procedures"
      },
      { 
        title: "Leave Policy (Revised)", 
        link: "/company policies/_14_33_50e319284d7e4fe4_Leave Policy (Revised).pdf", 
        description: "Comprehensive leave policy including all types of leaves"
      },
      { 
        title: "Local Conveyance Policy", 
        link: "/company policies/_15_9_02985794b8584650_Local Conveyance policy.pdf", 
        description: "Local travel and conveyance reimbursement guidelines"
      },
      { 
        title: "Whistle Blower Policy", 
        link: "/company policies/_16_4_3edd02c8f36f429f_Whistle Blower Policy.pdf", 
        description: "Whistleblower protection and reporting procedures"
      },
      { 
        title: "Tour Travel Policy", 
        link: "/company policies/_23_44_6eca6e909cee4aa7_Tour Travel Policy.pdf", 
        description: "Business travel guidelines and expense policies"
      },
      { 
        title: "Revised Attendance Policy", 
        link: "/company policies/_36_12_f19af68b04f849ee_Revised Attendance Policy w.e.f 21st May 25.pdf", 
        description: "Updated attendance policy effective from May 21, 2025"
      },
      { 
        title: "Night Shift Meal & Conveyance Allowance", 
        link: "/company policies/_38_0_62d66a9aaaf645cc_Meal and Conveyance for Employees Working at Night on Sites.pdf", 
        description: "Meal and conveyance allowance for employees working night shifts on sites"
      },
      { 
        title: "Flexible Work Schedule Policy", 
        link: "/company policies/Microsoft Word - Flexible Work Schedule.pdf", 
        description: "Guidelines for flexible working arrangements and remote work policies"
      },
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
        title: "Proposed Holiday List 2024", 
        link: "/company policies/Proposed Holiday List - 2024.xlsx.pdf", 
        description: "Proposed holiday calendar for the year 2024"
      }
    ]
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

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

      {/* Policy sections - All policies under HR POLICY without categorization */}
      <div className="space-y-6">
        {Object.entries(getPoliciesToDisplay()).map(([sectionTitle, sectionPolicies]) => {
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