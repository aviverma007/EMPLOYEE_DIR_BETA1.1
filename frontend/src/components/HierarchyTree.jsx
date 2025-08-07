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

  const cloudStyle = getCloudStyle(level);
  const marginLeft = level * 80;

  const getLevelIcon = (level) => {
    switch(level) {
      case 0: return <Crown className={`${cloudStyle.size.icon} text-white`} />;
      case 1: return <Star className={`${cloudStyle.size.icon} text-white`} />;
      case 2: return <Target className={`${cloudStyle.size.icon} text-white`} />;
      default: return <User className={`${cloudStyle.size.icon} text-white`} />;
    }
  };

  return (
    <div className="relative animate-pulse-gentle" style={{ marginLeft: `${marginLeft}px` }}>
      {/* Enhanced Connecting Lines */}
      {level > 0 && (
        <>
          {/* Horizontal cloud connector */}
          <div 
            className="absolute flex items-center"
            style={{
              left: -80,
              top: `${parseInt(cloudStyle.size.height.replace('h-', '')) * 4 + 8}px`,
              width: '80px',
              height: '4px'
            }}
          >
            {/* Dotted cloud line */}
            <div className="flex-1 border-t-2 border-dashed border-sky-300 opacity-70"></div>
            {/* Mini cloud connectors */}
            <div className="w-2 h-2 bg-white rounded-full border-2 border-sky-300 -ml-1"></div>
            <div className="w-3 h-3 bg-gradient-to-br from-sky-200 to-sky-300 rounded-full -ml-1"></div>
            <div className="w-2 h-2 bg-white rounded-full border-2 border-sky-300 -ml-1"></div>
          </div>
          
          {/* Vertical cloud connector */}
          <div 
            className="absolute"
            style={{
              left: -80,
              top: -40,
              width: '4px',
              height: `${parseInt(cloudStyle.size.height.replace('h-', '')) * 4 + 48}px`
            }}
          >
            <div className="w-full h-full border-l-2 border-dashed border-sky-300 opacity-70 relative">
              {/* Floating cloud elements along the line */}
              <div className="absolute w-2 h-2 bg-white rounded-full border border-sky-300 -left-1 top-4"></div>
              <div className="absolute w-1.5 h-1.5 bg-sky-200 rounded-full -left-0.5 top-8"></div>
              <div className="absolute w-2 h-2 bg-white rounded-full border border-sky-300 -left-1 top-12"></div>
            </div>
          </div>
        </>
      )}

      {/* Enhanced Cloud Container */}
      <div className="relative mb-10 group">
        {/* Cloud Shadow/Glow Effect */}
        <div className={`absolute inset-0 ${cloudStyle.size.width} ${cloudStyle.size.height} ${cloudStyle.colors.glow} rounded-full blur-lg opacity-30 group-hover:opacity-50 transition-all duration-500`}
             style={{ transform: 'scale(1.1)' }}>
        </div>

        {/* Main Cloud Shape */}
        <div className={`${cloudStyle.size.width} ${cloudStyle.size.height} relative`}>
          {/* Cloud Background with improved shape */}
          <div className={`absolute inset-0 bg-gradient-to-br ${cloudStyle.colors.gradient} ${cloudStyle.colors.border} border-2 shadow-2xl transform hover:scale-105 transition-all duration-300 hover:shadow-3xl hover:-rotate-1`}
               style={{
                 borderRadius: '50% 45% 55% 48% / 60% 50% 45% 40%',
                 filter: 'drop-shadow(0 8px 16px rgba(0,0,0,0.15))'
               }}>
            
            {/* Inner cloud highlights */}
            <div className="absolute top-2 left-4 w-6 h-4 bg-white bg-opacity-20 rounded-full blur-sm"></div>
            <div className="absolute top-3 right-6 w-4 h-3 bg-white bg-opacity-15 rounded-full blur-sm"></div>
          </div>
          
          {/* Cloud Content */}
          <div className="absolute inset-0 flex items-center justify-between px-6 py-3">
            {/* Employee Info Section */}
            <div className="flex items-center space-x-4 flex-1 min-w-0">
              {/* Enhanced Profile Section */}
              <div className="relative flex-shrink-0">
                {/* Profile Image Container */}
                <div className="w-12 h-12 rounded-full overflow-hidden bg-white bg-opacity-25 flex items-center justify-center border-3 border-white border-opacity-40 shadow-lg backdrop-blur-sm">
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
                  <div className="w-full h-full flex items-center justify-center" 
                       style={{display: employee.profileImage && employee.profileImage !== "/api/placeholder/150/150" ? 'none' : 'flex'}}>
                    {getLevelIcon(level)}
                  </div>
                </div>
                
                {/* Level Badge */}
                <div className="absolute -top-1 -right-1 w-5 h-5 bg-white rounded-full flex items-center justify-center border-2 border-current text-xs font-bold"
                     style={{ color: cloudStyle.colors.gradient.split(' ')[1].replace('from-', '').replace('-400', '-600') }}>
                  {level + 1}
                </div>
              </div>

              {/* Employee Details with Enhanced Typography */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <h3 className={`font-bold text-white ${cloudStyle.size.text} truncate drop-shadow-sm`}>
                    {employee.name}
                  </h3>
                  <Badge className="text-xs bg-white bg-opacity-25 text-white border-white border-opacity-40 backdrop-blur-sm px-2 py-0.5">
                    {employee.id}
                  </Badge>
                </div>
                
                <div className="space-y-0.5">
                  <p className={`${cloudStyle.size.text === 'text-base' ? 'text-sm' : 'text-xs'} text-white text-opacity-95 truncate font-medium drop-shadow-sm`}>
                    {employee.grade}
                  </p>
                  <p className={`${cloudStyle.size.text === 'text-base' ? 'text-sm' : 'text-xs'} text-white text-opacity-85 truncate flex items-center drop-shadow-sm`}>
                    <Building2 className="h-3 w-3 mr-1.5" />
                    {employee.department}
                  </p>
                  {employee.location && (
                    <p className={`${cloudStyle.size.text === 'text-base' ? 'text-sm' : 'text-xs'} text-white text-opacity-75 truncate`}>
                      📍 {employee.location}
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* Enhanced Control Section */}
            {hasChildren && (
              <div className="flex flex-col items-center space-y-2 flex-shrink-0">
                {/* Team Count Badge */}
                <Badge className="bg-white bg-opacity-25 text-white border-white border-opacity-40 text-xs backdrop-blur-sm px-2 py-1">
                  <Users className="h-3 w-3 mr-1" />
                  <span className="font-bold">{children.length}</span>
                  <span className="ml-1 text-xs opacity-75">team</span>
                </Badge>
                
                {/* Expand/Collapse Button */}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onToggle(employee.id)}
                  className="h-8 w-8 p-0 text-white hover:bg-white hover:bg-opacity-25 rounded-full transition-all duration-200 backdrop-blur-sm border border-white border-opacity-30"
                >
                  {isExpanded ? (
                    <ChevronUp className="h-4 w-4 drop-shadow-sm" />
                  ) : (
                    <ChevronDown className="h-4 w-4 drop-shadow-sm" />
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