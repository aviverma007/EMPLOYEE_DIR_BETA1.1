import React from "react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { 
  Rocket,
  Calendar,
  Bell,
  Sparkles
} from "lucide-react";

const ComingSoon = ({ title }) => {
  return (
    <div className="flex items-center justify-center h-96">
      <Card className="max-w-xl w-full mx-auto bg-gradient-to-br from-blue-50 via-white to-purple-50 border-2 border-blue-200 shadow-lg">
        <CardContent className="text-center py-12 px-6">
          <div className="space-y-4">
            {/* Animated Icon */}
            <div className="relative">
              <div className="p-4 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full w-fit mx-auto animate-pulse">
                <Rocket className="h-12 w-12 text-white" />
              </div>
              <div className="absolute -top-1 -right-1">
                <Sparkles className="h-6 w-6 text-yellow-500 animate-bounce" />
              </div>
            </div>

            {/* Title and Description */}
            <div className="space-y-2">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                {title} Coming Soon!
              </h1>
              <p className="text-sm text-gray-600 max-w-sm mx-auto">
                We're working hard to bring you something amazing. This feature is currently under development.
              </p>
            </div>

            {/* Features Preview */}
            <div className="grid grid-cols-3 gap-3 mt-6">
              <div className="p-3 bg-white rounded-lg shadow-sm border border-blue-100">
                <Calendar className="h-6 w-6 text-blue-500 mx-auto mb-1" />
                <h3 className="text-xs font-semibold text-gray-800">Planned Release</h3>
                <p className="text-xs text-gray-600">Q2 2025</p>
              </div>
              <div className="p-3 bg-white rounded-lg shadow-sm border border-purple-100">
                <Bell className="h-6 w-6 text-purple-500 mx-auto mb-1" />
                <h3 className="text-xs font-semibold text-gray-800">Get Notified</h3>
                <p className="text-xs text-gray-600">First to know</p>
              </div>
              <div className="p-3 bg-white rounded-lg shadow-sm border border-green-100">
                <Sparkles className="h-6 w-6 text-green-500 mx-auto mb-1" />
                <h3 className="text-xs font-semibold text-gray-800">New Features</h3>
                <p className="text-xs text-gray-600">Enhanced experience</p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-2 justify-center mt-6">
              <Button 
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-2 text-sm"
                onClick={() => {
                  // Handle notification signup
                  console.log("Signing up for notifications");
                }}
              >
                <Bell className="h-3 w-3 mr-1" />
                Notify Me When Ready
              </Button>
              <Button 
                variant="outline"
                className="border-blue-300 text-blue-600 hover:bg-blue-50 px-6 py-2 text-sm"
                onClick={() => {
                  // Handle feedback
                  console.log("Providing feedback");
                }}
              >
                Share Feedback
              </Button>
            </div>

            {/* Progress Indicator */}
            <div className="mt-6">
              <div className="text-xs text-gray-600 mb-1">Development Progress</div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full animate-pulse" style={{width: '45%'}}></div>
              </div>
              <div className="text-xs text-gray-500 mt-1">45% Complete</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ComingSoon;