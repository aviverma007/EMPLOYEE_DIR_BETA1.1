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
    <div className="min-h-[60vh] flex items-center justify-center">
      <Card className="max-w-2xl w-full mx-auto bg-gradient-to-br from-blue-50 via-white to-purple-50 border-2 border-blue-200 shadow-xl">
        <CardContent className="text-center py-16 px-8">
          <div className="space-y-6">
            {/* Animated Icon */}
            <div className="relative">
              <div className="p-6 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full w-fit mx-auto animate-pulse">
                <Rocket className="h-16 w-16 text-white" />
              </div>
              <div className="absolute -top-2 -right-2">
                <Sparkles className="h-8 w-8 text-yellow-500 animate-bounce" />
              </div>
            </div>

            {/* Title and Description */}
            <div className="space-y-3">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                {title} Coming Soon!
              </h1>
              <p className="text-xl text-gray-600 max-w-lg mx-auto">
                We're working hard to bring you something amazing. This feature is currently under development.
              </p>
            </div>

            {/* Features Preview */}
            <div className="grid md:grid-cols-3 gap-4 mt-8">
              <div className="p-4 bg-white rounded-lg shadow-sm border border-blue-100">
                <Calendar className="h-8 w-8 text-blue-500 mx-auto mb-2" />
                <h3 className="font-semibold text-gray-800">Planned Release</h3>
                <p className="text-sm text-gray-600">Q2 2025</p>
              </div>
              <div className="p-4 bg-white rounded-lg shadow-sm border border-purple-100">
                <Bell className="h-8 w-8 text-purple-500 mx-auto mb-2" />
                <h3 className="font-semibold text-gray-800">Get Notified</h3>
                <p className="text-sm text-gray-600">First to know</p>
              </div>
              <div className="p-4 bg-white rounded-lg shadow-sm border border-green-100">
                <Sparkles className="h-8 w-8 text-green-500 mx-auto mb-2" />
                <h3 className="font-semibold text-gray-800">New Features</h3>
                <p className="text-sm text-gray-600">Enhanced experience</p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 justify-center mt-8">
              <Button 
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-2"
                onClick={() => {
                  // Handle notification signup
                  console.log("Signing up for notifications");
                }}
              >
                <Bell className="h-4 w-4 mr-2" />
                Notify Me When Ready
              </Button>
              <Button 
                variant="outline"
                className="border-blue-300 text-blue-600 hover:bg-blue-50 px-8 py-2"
                onClick={() => {
                  // Handle feedback
                  console.log("Providing feedback");
                }}
              >
                Share Feedback
              </Button>
            </div>

            {/* Progress Indicator */}
            <div className="mt-8">
              <div className="text-sm text-gray-600 mb-2">Development Progress</div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full animate-pulse" style={{width: '45%'}}></div>
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