import React from "react";
import { User, ChevronDown, ChevronRight } from "lucide-react";
import { Badge } from "./ui/badge";
import { useState } from "react";

const TreeNode = ({ employee, children, level = 0 }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const hasChildren = children && children.length > 0;

  return (
    <div className="relative">
      {/* Node Content */}
      <div 
        className="flex items-center space-x-3 p-3 hover:bg-slate-50 rounded-lg transition-colors cursor-pointer"
        style={{ marginLeft: level * 24 }}
        onClick={() => hasChildren && setIsExpanded(!isExpanded)}
      >
        {/* Expansion Icon */}
        <div className="w-5 h-5 flex items-center justify-center">
          {hasChildren ? (
            isExpanded ? (
              <ChevronDown className="h-4 w-4 text-gray-500" />
            ) : (
              <ChevronRight className="h-4 w-4 text-gray-500" />
            )
          ) : (
            <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
          )}
        </div>

        {/* Profile Image */}
        <div className="w-8 h-8 rounded-full overflow-hidden bg-gradient-to-br from-blue-200 to-blue-300 flex items-center justify-center flex-shrink-0">
          {employee.profileImage && employee.profileImage !== "/api/placeholder/150/150" ? (
            <img 
              src={employee.profileImage} 
              alt={employee.name}
              className="w-full h-full object-cover"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'flex';
              }}
            />
          ) : null}
          <User className="h-4 w-4 text-blue-500" style={{display: employee.profileImage && employee.profileImage !== "/api/placeholder/150/150" ? 'none' : 'block'}} />
        </div>

        {/* Employee Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2">
            <p className="font-medium text-blue-900 truncate">{employee.name}</p>
            <Badge variant="outline" className="text-xs flex-shrink-0 border-blue-200 text-blue-700">{employee.id}</Badge>
          </div>
          <p className="text-sm text-blue-600 truncate">{employee.grade}</p>
          <p className="text-xs text-blue-500">{employee.department}</p>
        </div>

        {/* Children Count */}
        {hasChildren && (
          <Badge variant="secondary" className="text-xs bg-blue-100 text-blue-700">
            {children.length} {children.length === 1 ? 'report' : 'reports'}
          </Badge>
        )}
      </div>

      {/* Children */}
      {hasChildren && isExpanded && (
        <div className="relative">
          {/* Vertical Line */}
          {level >= 0 && (
            <div 
              className="absolute w-px bg-gray-200"
              style={{
                left: level * 24 + 12,
                top: 0,
                height: '100%'
              }}
            />
          )}
          
          {children.map((child, index) => (
            <div key={child.id} className="relative">
              {/* Horizontal Line */}
              <div 
                className="absolute w-3 h-px bg-gray-200"
                style={{
                  left: level * 24 + 12,
                  top: 24
                }}
              />
              <TreeNode 
                employee={child} 
                children={[]} 
                level={level + 1} 
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const HierarchyTree = ({ hierarchyStructure }) => {
  const { topLevel, childrenMap } = hierarchyStructure;

  if (topLevel.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <User className="h-12 w-12 mx-auto mb-4 opacity-50" />
        <p>No hierarchy structure to display.</p>
      </div>
    );
  }

  const buildTree = (employee) => {
    const children = childrenMap.get(employee.id) || [];
    return (
      <TreeNode 
        key={employee.id}
        employee={employee} 
        children={children}
      />
    );
  };

  return (
    <div className="space-y-4">
      <div className="bg-slate-50 p-4 rounded-lg">
        <h4 className="font-medium text-slate-900 mb-4">Organizational Structure</h4>
        <div className="space-y-2">
          {topLevel.map(employee => buildTree(employee))}
        </div>
      </div>
    </div>
  );
};

export default HierarchyTree;