import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { 
  Workflow,
  ArrowRight,
  Clock,
  Users,
  CheckCircle,
  AlertCircle
} from "lucide-react";

const Workflows = () => {
  const workflows = [
    {
      title: "Employee Onboarding",
      description: "Complete process for new employee integration",
      steps: 5,
      duration: "3-5 days",
      status: "active",
      participants: ["HR", "IT", "Manager", "Buddy"]
    },
    {
      title: "Leave Approval",
      description: "Standard leave request and approval workflow",
      steps: 3,
      duration: "1-2 days",
      status: "active",
      participants: ["Employee", "Manager", "HR"]
    },
    {
      title: "Expense Reimbursement",
      description: "Process for expense claims and reimbursements",
      steps: 4,
      duration: "5-7 days",
      status: "active",
      participants: ["Employee", "Manager", "Finance"]
    },
    {
      title: "Performance Review",
      description: "Annual performance evaluation process",
      steps: 6,
      duration: "2-3 weeks",
      status: "scheduled",
      participants: ["Employee", "Manager", "HR", "Senior Management"]
    }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'text-green-600 bg-green-100';
      case 'scheduled':
        return 'text-blue-600 bg-blue-100';
      case 'pending':
        return 'text-yellow-600 bg-yellow-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="h-4 w-4" />;
      case 'scheduled':
        return <Clock className="h-4 w-4" />;
      case 'pending':
        return <AlertCircle className="h-4 w-4" />;
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center space-x-3 mb-4">
          <div className="p-3 bg-blue-100 rounded-full">
            <Workflow className="h-8 w-8 text-blue-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800">Workflows</h1>
        </div>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Streamlined processes to ensure efficiency and consistency across all operations
        </p>
      </div>

      {/* Workflows Grid */}
      <div className="grid gap-6 md:grid-cols-2">
        {workflows.map((workflow, index) => (
          <Card key={index} className="hover:shadow-lg transition-all duration-300 border-2 border-gray-100 hover:border-blue-200">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg font-bold text-gray-800 mb-2">
                    {workflow.title}
                  </CardTitle>
                  <p className="text-sm text-gray-600 mb-3">
                    {workflow.description}
                  </p>
                  <div className={`inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(workflow.status)}`}>
                    {getStatusIcon(workflow.status)}
                    <span className="capitalize">{workflow.status}</span>
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Workflow Stats */}
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{workflow.steps}</div>
                  <div className="text-xs text-gray-600">Steps</div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-sm font-bold text-blue-600">{workflow.duration}</div>
                  <div className="text-xs text-gray-600">Duration</div>
                </div>
              </div>

              {/* Participants */}
              <div>
                <div className="flex items-center space-x-2 mb-2">
                  <Users className="h-4 w-4 text-gray-500" />
                  <span className="text-sm font-medium text-gray-700">Participants</span>
                </div>
                <div className="flex flex-wrap gap-1">
                  {workflow.participants.map((participant, idx) => (
                    <span 
                      key={idx}
                      className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full"
                    >
                      {participant}
                    </span>
                  ))}
                </div>
              </div>

              {/* Action Button */}
              <Button 
                className="w-full mt-4 bg-blue-600 hover:bg-blue-700"
                onClick={() => {
                  console.log(`Opening workflow: ${workflow.title}`);
                  // Handle workflow opening logic
                }}
              >
                View Workflow
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Coming Soon Section */}
      <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200">
        <CardContent className="text-center py-12">
          <div className="space-y-4">
            <div className="p-4 bg-blue-100 rounded-full w-fit mx-auto">
              <Workflow className="h-12 w-12 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-800">More Workflows Coming Soon</h3>
            <p className="text-gray-600 max-w-md mx-auto">
              We're continuously improving our processes. New workflows for project management, 
              vendor onboarding, and more are in development.
            </p>
            <Button variant="outline" className="mt-4">
              Request New Workflow
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Workflows;