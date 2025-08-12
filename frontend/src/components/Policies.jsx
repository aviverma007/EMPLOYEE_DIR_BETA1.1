import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { 
  ChevronLeft, 
  ChevronRight, 
  ChevronDown,
  ChevronRight as ChevronRightIcon,
  FileText,
  Users,
  Monitor,
  Shield,
  Folder
} from "lucide-react";

const Policies = () => {
  const [currentBannerIndex, setCurrentBannerIndex] = useState(0);
  const [expandedSections, setExpandedSections] = useState({});

  // Policy banner images
  const bannerImages = [
    "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1200&h=300&fit=crop&crop=center",
    "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1200&h=300&fit=crop&crop=center",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&h=300&fit=crop&crop=center",
    "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=1200&h=300&fit=crop&crop=center"
  ];

  // Auto-scroll banner every 3 seconds  
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentBannerIndex(prev => (prev + 1) % bannerImages.length);
    }, 3000);
    return () => clearInterval(interval);
  }, [bannerImages.length]);

  // Navigate banner manually
  const navigateBanner = (direction) => {
    if (direction === 'next') {
      setCurrentBannerIndex(prev => (prev + 1) % bannerImages.length);
    } else {
      setCurrentBannerIndex(prev => (prev - 1 + bannerImages.length) % bannerImages.length);
    }
  };

  // Toggle section expansion
  const toggleSection = (sectionKey) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionKey]: !prev[sectionKey]
    }));
  };

  // Policy sections data
  const policySections = [
    {
      key: "hr",
      title: "HR POLICY",
      icon: <Users className="h-5 w-5" />,
      color: "text-blue-600",
      bgColor: "bg-blue-50",
      borderColor: "border-blue-200",
      links: [
        { title: "Employee Handbook", url: "#" },
        { title: "Leave and Attendance Policy", url: "#" },
        { title: "Performance Management", url: "#" },
        { title: "Code of Conduct", url: "#" },
        { title: "Grievance Policy", url: "#" }
      ]
    },
    {
      key: "it",
      title: "IT POLICY",
      icon: <Monitor className="h-5 w-5" />,
      color: "text-green-600",
      bgColor: "bg-green-50",
      borderColor: "border-green-200",
      links: [
        { title: "IT Security Guidelines", url: "#" },
        { title: "Data Protection Policy", url: "#" },
        { title: "Software Usage Policy", url: "#" },
        { title: "Network Access Guidelines", url: "#" },
        { title: "Email and Internet Usage", url: "#" }
      ]
    },
    {
      key: "admin",
      title: "ADMIN POLICY",
      icon: <Shield className="h-5 w-5" />,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
      borderColor: "border-purple-200",
      links: [
        { title: "Office Management Policy", url: "#" },
        { title: "Travel and Expense Policy", url: "#" },
        { title: "Asset Management Guidelines", url: "#" },
        { title: "Vendor Management Policy", url: "#" },
        { title: "Document Control Procedures", url: "#" }
      ]
    },
    {
      key: "other",
      title: "OTHER POLICIES",
      icon: <Folder className="h-5 w-5" />,
      color: "text-orange-600",
      bgColor: "bg-orange-50",
      borderColor: "border-orange-200",
      links: [
        { title: "Health and Safety Policy", url: "#" },
        { title: "Environmental Policy", url: "#" },
        { title: "Quality Management System", url: "#" },
        { title: "Training and Development", url: "#" },
        { title: "Communication Policy", url: "#" }
      ]
    }
  ];

  return (
    <div className="space-y-4">
      {/* Compact Policy Banner Section */}
      <div className="relative w-full h-48 rounded-lg shadow-md overflow-hidden">
        <div 
          className="flex transition-transform duration-500 ease-in-out h-full"
          style={{ transform: `translateX(-${currentBannerIndex * 100}%)` }}
        >
          {bannerImages.map((image, index) => (
            <div
              key={index}
              className="min-w-full h-full relative"
              style={{
                backgroundImage: `url(${image})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center'
              }}
            >
              <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <div className="text-center text-white">
                  <h2 className="text-3xl font-bold mb-2">Company Policies</h2>
                  <p className="text-lg">Guidelines for Excellence and Compliance</p>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Navigation Arrows */}
        <button
          onClick={() => navigateBanner('prev')}
          className="absolute left-3 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full p-1.5 transition-all"
        >
          <ChevronLeft className="h-5 w-5 text-gray-800" />
        </button>
        <button
          onClick={() => navigateBanner('next')}
          className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full p-1.5 transition-all"
        >
          <ChevronRight className="h-5 w-5 text-gray-800" />
        </button>
        
        {/* Dots Indicator */}
        <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 flex space-x-1.5">
          {bannerImages.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentBannerIndex(index)}
              className={`w-2.5 h-2.5 rounded-full transition-all ${
                index === currentBannerIndex ? 'bg-white' : 'bg-white bg-opacity-50'
              }`}
            />
          ))}
        </div>
      </div>

      {/* Compact Policy Tree Section */}
      <div className="space-y-3">
        <div className="text-center mb-4">
          <h3 className="text-xl font-bold text-gray-800 mb-1">Policy Directory</h3>
          <p className="text-sm text-gray-600">Click on any policy category to view available documents</p>
        </div>

        <div className="grid gap-3">
          {policySections.map((section) => (
            <Card 
              key={section.key}
              className={`transition-all duration-300 hover:shadow-lg ${section.borderColor} border-2`}
            >
              <CardHeader className="pb-2">
                <Button
                  variant="ghost"
                  onClick={() => toggleSection(section.key)}
                  className={`w-full justify-start p-0 h-auto hover:bg-transparent`}
                >
                  <div className={`flex items-center space-x-3 w-full p-3 rounded-lg ${section.bgColor} hover:opacity-80 transition-opacity`}>
                    <div className={`${section.color}`}>
                      {section.icon}
                    </div>
                    <div className="flex-1 text-left">
                      <CardTitle className={`text-base font-bold ${section.color}`}>
                        {section.title}
                      </CardTitle>
                    </div>
                    <div className={`${section.color}`}>
                      {expandedSections[section.key] ? (
                        <ChevronDown className="h-4 w-4" />
                      ) : (
                        <ChevronRightIcon className="h-4 w-4" />
                      )}
                    </div>
                  </div>
                </Button>
              </CardHeader>
              
              {expandedSections[section.key] && (
                <CardContent className="pt-0">
                  <div className="space-y-2 pl-6">
                    {section.links.map((link, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <FileText className={`h-3 w-3 ${section.color}`} />
                        <a
                          href={link.url}
                          className={`${section.color} hover:underline text-sm font-medium transition-all hover:translate-x-1`}
                          onClick={(e) => {
                            e.preventDefault();
                            // Handle PDF opening logic here
                            console.log(`Opening: ${link.title}`);
                          }}
                        >
                          {link.title}
                        </a>
                      </div>
                    ))}
                  </div>
                </CardContent>
              )}
            </Card>
          ))}
        </div>
      </div>

      {/* Footer Note */}
      <div className="text-center py-2">
        <p className="text-xs text-gray-500">
          For any policy-related queries, please contact the HR department
        </p>
      </div>
    </div>
  );
};

export default Policies;