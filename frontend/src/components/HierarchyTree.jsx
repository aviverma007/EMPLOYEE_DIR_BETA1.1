import React, { useState } from "react";
import { User, ChevronDown, ChevronUp, Users, Building2, Crown, Star, Target } from "lucide-react";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";

const CloudNode = ({ employee, children, level = 0, isExpanded, onToggle }) => {
  const hasChildren = children && children.length > 0;
  
  const getCloudStyle = (level) => {
    const cloudColors = [
      {
        gradient: 'from-sky-400 via-sky-500 to-sky-600',
        glow: 'shadow-sky-200',
        border: 'border-sky-300',
        accent: 'bg-sky-100'
      },
      {
        gradient: 'from-emerald-400 via-emerald-500 to-emerald-600',
        glow: 'shadow-emerald-200',
        border: 'border-emerald-300',
        accent: 'bg-emerald-100'
      },
      {
        gradient: 'from-violet-400 via-violet-500 to-violet-600',
        glow: 'shadow-violet-200',
        border: 'border-violet-300',
        accent: 'bg-violet-100'
      },
      {
        gradient: 'from-amber-400 via-amber-500 to-amber-600',
        glow: 'shadow-amber-200',
        border: 'border-amber-300',
        accent: 'bg-amber-100'
      },
      {
        gradient: 'from-rose-400 via-rose-500 to-rose-600',
        glow: 'shadow-rose-200',
        border: 'border-rose-300',
        accent: 'bg-rose-100'
      },
      {
        gradient: 'from-indigo-400 via-indigo-500 to-indigo-600',
        glow: 'shadow-indigo-200',
        border: 'border-indigo-300',
        accent: 'bg-indigo-100'
      },
      {
        gradient: 'from-teal-400 via-teal-500 to-teal-600',
        glow: 'shadow-teal-200',
        border: 'border-teal-300',
        accent: 'bg-teal-100'
      }
    ];
    
    const sizes = [
      { width: 'w-80', height: 'h-24', text: 'text-base', icon: 'h-6 w-6' }, // Level 0 - CEO/Top
      { width: 'w-72', height: 'h-22', text: 'text-sm', icon: 'h-5 w-5' },   // Level 1 - Directors
      { width: 'w-64', height: 'h-20', text: 'text-sm', icon: 'h-5 w-5' },   // Level 2 - Managers
      { width: 'w-56', height: 'h-18', text: 'text-sm', icon: 'h-4 w-4' },   // Level 3 - Leads
      { width: 'w-48', height: 'h-16', text: 'text-xs', icon: 'h-4 w-4' },   // Level 4+ - Contributors
    ];
    
    return {
      colors: cloudColors[level % cloudColors.length],
      size: sizes[Math.min(level, sizes.length - 1)],
      level: level
    };
  };

  const cloudStyle = getCloudStyle(level);
  const marginLeft = level * 60;

  return (
    <div className="relative" style={{ marginLeft: `${marginLeft}px` }}>
      {/* Connecting Lines */}
      {level > 0 && (
        <>
          {/* Horizontal line to parent */}
          <div 
            className="absolute bg-gradient-to-r from-blue-300 to-blue-400 h-0.5 rounded-full"
            style={{
              left: -60,
              top: '40px',
              width: '60px'
            }}
          />
          {/* Vertical line from parent */}
          <div 
            className="absolute bg-gradient-to-b from-blue-300 to-blue-400 w-0.5 rounded-full"
            style={{
              left: -60,
              top: -20,
              height: '60px'
            }}
          />
        </>
      )}

      {/* Cloud Container */}
      <div className="relative mb-8">
        {/* Cloud Shape */}
        <div className={`${cloudStyle.size} relative`}>
          <div className={`absolute inset-0 bg-gradient-to-br ${cloudStyle.color} rounded-full shadow-lg transform hover:scale-105 transition-all duration-300 hover:shadow-xl`}
               style={{
                 clipPath: 'ellipse(100% 85% at 50% 50%)',
                 filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.1))'
               }}>
          </div>
          
          {/* Cloud Content */}
          <div className="absolute inset-0 flex items-center justify-between px-4 py-2">
            {/* Employee Info */}
            <div className="flex items-center space-x-3 flex-1 min-w-0">
              {/* Profile Image */}
              <div className="w-10 h-10 rounded-full overflow-hidden bg-white bg-opacity-20 flex items-center justify-center flex-shrink-0 border-2 border-white border-opacity-30">
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
                <User className="h-5 w-5 text-white" style={{display: employee.profileImage && employee.profileImage !== "/api/placeholder/150/150" ? 'none' : 'block'}} />
              </div>

              {/* Employee Details */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2">
                  <p className="font-semibold text-white text-sm truncate">{employee.name}</p>
                  <Badge variant="secondary" className="text-xs bg-white bg-opacity-20 text-white border-white border-opacity-30">
                    {employee.id}
                  </Badge>
                </div>
                <p className="text-xs text-white text-opacity-90 truncate">{employee.grade}</p>
                <p className="text-xs text-white text-opacity-75 truncate flex items-center">
                  <Building2 className="h-3 w-3 mr-1" />
                  {employee.department}
                </p>
              </div>
            </div>

            {/* Expand/Collapse Button */}
            {hasChildren && (
              <div className="flex items-center space-x-2">
                <Badge className="bg-white bg-opacity-20 text-white border-white border-opacity-30 text-xs">
                  <Users className="h-3 w-3 mr-1" />
                  {children.length}
                </Badge>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onToggle(employee.id)}
                  className="h-6 w-6 p-0 text-white hover:bg-white hover:bg-opacity-20 rounded-full"
                >
                  {isExpanded ? (
                    <ChevronUp className="h-4 w-4" />
                  ) : (
                    <ChevronDown className="h-4 w-4" />
                  )}
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Child Nodes */}
        {hasChildren && isExpanded && (
          <div className="mt-6 space-y-4">
            {/* Vertical line for children */}
            <div 
              className="absolute bg-gradient-to-b from-blue-300 to-blue-400 w-0.5 rounded-full"
              style={{
                left: '50%',
                top: cloudStyle.size.includes('72') ? '80px' : 
                     cloudStyle.size.includes('64') ? '72px' :
                     cloudStyle.size.includes('56') ? '64px' :
                     cloudStyle.size.includes('48') ? '56px' : '48px',
                height: `${children.length * 100}px`,
                transform: 'translateX(-50%)'
              }}
            />
            
            {children.map((child, index) => (
              <CloudNode 
                key={child.id}
                employee={child} 
                children={[]} // For now, only show direct reports
                level={level + 1}
                isExpanded={true}
                onToggle={() => {}}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const HierarchyTree = ({ hierarchyStructure }) => {
  const [expandedNodes, setExpandedNodes] = useState(new Set());
  const { topLevel, childrenMap } = hierarchyStructure;

  const toggleNode = (nodeId) => {
    const newExpanded = new Set(expandedNodes);
    if (newExpanded.has(nodeId)) {
      newExpanded.delete(nodeId);
    } else {
      newExpanded.add(nodeId);
    }
    setExpandedNodes(newExpanded);
  };

  // Initialize all nodes as expanded for better visualization
  React.useEffect(() => {
    const allNodeIds = new Set();
    const addNodeIds = (nodes) => {
      nodes.forEach(node => {
        allNodeIds.add(node.id);
        const children = childrenMap.get(node.id) || [];
        addNodeIds(children);
      });
    };
    addNodeIds(topLevel);
    setExpandedNodes(allNodeIds);
  }, [topLevel, childrenMap]);

  if (topLevel.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <div className="relative">
          <div className="w-32 h-16 bg-gradient-to-br from-gray-300 to-gray-400 rounded-full mx-auto mb-4 opacity-50 flex items-center justify-center"
               style={{
                 clipPath: 'ellipse(100% 85% at 50% 50%)',
                 filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))'
               }}>
            <User className="h-8 w-8 text-white" />
          </div>
        </div>
        <p className="text-lg font-medium">No hierarchy structure to display</p>
        <p className="text-sm">Add reporting relationships to see the organizational cloud structure.</p>
      </div>
    );
  }

  const buildCloudTree = (employee) => {
    const children = childrenMap.get(employee.id) || [];
    return (
      <CloudNode 
        key={employee.id}
        employee={employee} 
        children={children}
        level={0}
        isExpanded={expandedNodes.has(employee.id)}
        onToggle={toggleNode}
      />
    );
  };

  return (
    <div className="relative bg-gradient-to-br from-blue-50 via-white to-purple-50 p-8 rounded-lg border border-blue-200 overflow-x-auto">
      <div className="flex flex-col space-y-8 min-w-max">
        <div className="text-center mb-6">
          <h4 className="text-xl font-bold text-blue-900 mb-2">Organizational Cloud Structure</h4>
          <p className="text-blue-600">Interactive hierarchy visualization with reporting relationships</p>
        </div>
        
        <div className="space-y-12">
          {topLevel.map(employee => buildCloudTree(employee))}
        </div>
      </div>
      
      {/* Background decorative elements */}
      <div className="absolute top-4 right-4 w-16 h-8 bg-gradient-to-br from-blue-200 to-blue-300 rounded-full opacity-20"
           style={{ clipPath: 'ellipse(100% 85% at 50% 50%)' }}>
      </div>
      <div className="absolute bottom-4 left-4 w-20 h-10 bg-gradient-to-br from-purple-200 to-purple-300 rounded-full opacity-20"
           style={{ clipPath: 'ellipse(100% 85% at 50% 50%)' }}>
      </div>
    </div>
  );
};

export default HierarchyTree;