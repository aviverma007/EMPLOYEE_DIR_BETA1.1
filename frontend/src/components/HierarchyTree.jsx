import React, { useState } from "react";
import { User, ChevronDown, ChevronUp, Users, Building2 } from "lucide-react";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";

const BoxNode = ({ employee, children, level = 0, isExpanded, onToggle }) => {
  const hasChildren = children && children.length > 0;
  
  const getBoxStyle = (level) => {
    const sizes = [
      { width: 'w-80', height: 'h-24', text: 'text-base' }, // Level 0 - CEO/Top
      { width: 'w-72', height: 'h-20', text: 'text-sm' },   // Level 1 - Directors
      { width: 'w-64', height: 'h-18', text: 'text-sm' },   // Level 2 - Managers
      { width: 'w-56', height: 'h-16', text: 'text-sm' },   // Level 3 - Leads
      { width: 'w-48', height: 'h-14', text: 'text-xs' },   // Level 4+ - Contributors
    ];
    
    return {
      size: sizes[Math.min(level, sizes.length - 1)]
    };
  };

  const boxStyle = getBoxStyle(level);
  const marginLeft = level * 60;

  return (
    <div className="relative" style={{ marginLeft: `${marginLeft}px` }}>
      {/* Simple connecting lines */}
      {level > 0 && (
        <>
          {/* Horizontal line to parent */}
          <div 
            className="absolute bg-gray-600 h-0.5"
            style={{
              left: -60,
              top: `${parseInt(boxStyle.size.height.replace('h-', '')) * 4 + 8}px`,
              width: '60px'
            }}
          />
          
          {/* Vertical line from parent */}
          <div 
            className="absolute bg-gray-600 w-0.5"
            style={{
              left: -60,
              top: -30,
              height: `${parseInt(boxStyle.size.height.replace('h-', '')) * 4 + 38}px`
            }}
          />
        </>
      )}

      {/* Blue Box Container */}
      <div className="relative mb-8">
        {/* Main Blue Box */}
        <div className={`${boxStyle.size.width} ${boxStyle.size.height} relative`}>
          {/* Blue Background Box */}
          <div className="absolute inset-0 bg-blue-600 border-2 border-blue-700 rounded-lg shadow-lg">
          </div>
          
          {/* Box Content */}
          <div className="absolute inset-0 flex items-center justify-between px-4 py-2">
            {/* Employee Info Section */}
            <div className="flex items-center space-x-3 flex-1 min-w-0">
              {/* Profile Image */}
              <div className="w-10 h-10 rounded-full overflow-hidden bg-white flex items-center justify-center border-2 border-white flex-shrink-0">
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
                <User className="h-5 w-5 text-gray-600" 
                     style={{display: employee.profileImage && employee.profileImage !== "/api/placeholder/150/150" ? 'none' : 'flex'}} />
              </div>

              {/* Employee Details */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <h3 className={`font-bold text-white ${boxStyle.size.text} truncate`}>
                    {employee.name}
                  </h3>
                  <Badge className="text-xs bg-white text-black border-white px-2 py-0.5">
                    {employee.id}
                  </Badge>
                </div>
                
                <div className="space-y-0.5">
                  <p className={`${boxStyle.size.text === 'text-base' ? 'text-sm' : 'text-xs'} text-gray-100 truncate font-medium`}>
                    {employee.grade}
                  </p>
                  <p className={`${boxStyle.size.text === 'text-base' ? 'text-sm' : 'text-xs'} text-gray-200 truncate flex items-center`}>
                    <Building2 className="h-3 w-3 mr-1.5" />
                    {employee.department}
                  </p>
                  {employee.location && (
                    <p className={`${boxStyle.size.text === 'text-base' ? 'text-sm' : 'text-xs'} text-gray-300 truncate`}>
                      📍 {employee.location}
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* Control Section */}
            {hasChildren && (
              <div className="flex flex-col items-center space-y-2 flex-shrink-0">
                {/* Team Count Badge */}
                <Badge className="bg-white text-black border-white text-xs px-2 py-1">
                  <Users className="h-3 w-3 mr-1" />
                  <span className="font-bold">{children.length}</span>
                </Badge>
                
                {/* Expand/Collapse Button */}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onToggle(employee.id)}
                  className="h-6 w-6 p-0 text-white hover:bg-white hover:bg-opacity-20 rounded border border-white border-opacity-30"
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

        {/* Enhanced Children Section */}
        {hasChildren && isExpanded && (
          <div className="mt-8 space-y-6 relative">
            {/* Enhanced vertical connection line for children */}
            <div 
              className="absolute z-0"
              style={{
                left: '50%',
                top: '-20px',
                transform: 'translateX(-50%)'
              }}
            >
              {/* Main trunk */}
              <div className="w-1 bg-gradient-to-b from-sky-300 via-sky-400 to-transparent rounded-full"
                   style={{ height: `${Math.max(children.length * 120, 60)}px` }}>
              </div>
              
              {/* Cloud particles along the trunk */}
              {[...Array(Math.ceil(children.length / 2))].map((_, i) => (
                <div key={i} 
                     className="absolute w-3 h-3 bg-gradient-to-br from-white to-sky-200 rounded-full border border-sky-300 shadow-sm animate-float"
                     style={{ 
                       left: '-6px', 
                       top: `${20 + i * 40}px`,
                       animationDelay: `${i * 0.5}s`
                     }}>
                </div>
              ))}
            </div>
            
            {/* Child nodes with staggered animation */}
            <div className="relative z-10 space-y-6">
              {children.map((child, index) => (
                <div key={child.id} 
                     className="animate-slide-in-right"
                     style={{ 
                       animationDelay: `${index * 0.1}s`,
                       animationFillMode: 'both'
                     }}>
                  <CloudNode 
                    employee={child} 
                    children={[]} // For now, only show direct reports
                    level={level + 1}
                    isExpanded={true}
                    onToggle={() => {}}
                  />
                </div>
              ))}
            </div>
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
      <div className="text-center py-16 text-gray-500 relative">
        {/* Background cloud elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-8 left-1/4 w-16 h-10 bg-gradient-to-br from-sky-200 to-sky-300 rounded-full opacity-20 animate-float-slow"
               style={{ borderRadius: '60% 40% 70% 30% / 60% 30% 40% 70%' }}>
          </div>
          <div className="absolute top-16 right-1/4 w-12 h-8 bg-gradient-to-br from-blue-200 to-blue-300 rounded-full opacity-15 animate-float-slower"
               style={{ borderRadius: '50% 60% 40% 80% / 70% 40% 60% 30%' }}>
          </div>
        </div>
        
        <div className="relative z-10">
          <div className="w-40 h-24 bg-gradient-to-br from-gray-300 via-gray-400 to-gray-500 mx-auto mb-6 opacity-40 flex items-center justify-center shadow-lg"
               style={{
                 borderRadius: '50% 45% 55% 48% / 60% 50% 45% 40%',
                 filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.1))'
               }}>
            <User className="h-12 w-12 text-white" />
          </div>
          <h3 className="text-xl font-bold mb-2 text-gray-600">No hierarchy structure to display</h3>
          <p className="text-gray-500 max-w-md mx-auto leading-relaxed">
            Add reporting relationships above to see the beautiful organizational cloud structure come to life.
          </p>
          <div className="mt-4 text-sm text-gray-400">
            ☁️ Create connections • 🌟 Watch the magic happen
          </div>
        </div>
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
    <div className="relative bg-gradient-to-br from-sky-50 via-white via-blue-50 to-indigo-50 p-8 rounded-xl border-2 border-sky-200 overflow-x-auto shadow-inner">
      {/* Enhanced Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Floating background clouds */}
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className={`absolute bg-gradient-to-br from-white to-sky-100 rounded-full opacity-30 animate-float-${i % 3}`}
            style={{
              width: `${Math.random() * 60 + 20}px`,
              height: `${Math.random() * 30 + 15}px`,
              left: `${Math.random() * 90}%`,
              top: `${Math.random() * 90}%`,
              borderRadius: `${Math.random() * 30 + 40}% ${Math.random() * 30 + 40}% ${Math.random() * 30 + 40}% ${Math.random() * 30 + 40}% / ${Math.random() * 30 + 40}% ${Math.random() * 30 + 40}% ${Math.random() * 30 + 40}% ${Math.random() * 30 + 40}%`,
              animationDelay: `${Math.random() * 5}s`
            }}
          />
        ))}
        
        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-sky-50 opacity-40"></div>
      </div>
      
      <div className="relative z-10 flex flex-col space-y-10 min-w-max">
        {/* Enhanced Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center space-x-3 bg-white bg-opacity-60 backdrop-blur-sm px-6 py-3 rounded-full border border-sky-200 shadow-lg mb-4">
            <div className="w-8 h-5 bg-gradient-to-br from-sky-400 to-sky-600 rounded-full" 
                 style={{ borderRadius: '60% 40% 70% 30% / 60% 30% 40% 70%' }}>
            </div>
            <h4 className="text-xl font-bold text-sky-900">Organizational Cloud Structure</h4>
            <div className="w-6 h-4 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full" 
                 style={{ borderRadius: '50% 60% 40% 80% / 70% 40% 60% 30%' }}>
            </div>
          </div>
          <p className="text-sky-700 font-medium">Interactive hierarchy visualization with cloud-based connections</p>
        </div>
        
        {/* Cloud Structure */}
        <div className="space-y-16 relative">
          {topLevel.map((employee, index) => (
            <div key={employee.id} 
                 className="animate-fade-in-up"
                 style={{ animationDelay: `${index * 0.2}s` }}>
              {buildCloudTree(employee)}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HierarchyTree;