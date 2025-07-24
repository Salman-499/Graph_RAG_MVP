interface StepwiseLogoProps {
  width?: number;
  height?: number;
  className?: string;
}

export default function StepwiseLogo({ width = 40, height = 32, className = '' }: StepwiseLogoProps) {
  return (
    <svg 
      width={width} 
      height={height} 
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Subtle background circle */}
      <circle cx="50" cy="50" r="45" fill="#e0f0ff" stroke="#d0e0ff" strokeWidth="1.5"/>
      
      {/* Dotted cross (x-y axis) through center node */}
      <g stroke="#007FFF" strokeWidth="2.5" strokeDasharray="0,0" opacity="0.3">
        {/* Horizontal axis */}
        <line x1="5" y1="50" x2="95" y2="50"/>
        {/* Vertical axis */}
        <line x1="50" y1="5" x2="50" y2="95"/>
      </g>
      
      <g stroke="#007FFF" strokeWidth="5" strokeLinecap="round">
        {/* Start from bottom-left, go RIGHT first */}
        <line x1="25" y1="75" x2="50" y2="75"/>
        
        {/* Then go UP */}
        <line x1="50" y1="75" x2="50" y2="50"/>
        
        {/* Then go RIGHT again */}
        <line x1="50" y1="50" x2="75" y2="50"/>
        
        {/* Finally go UP */}
        <line x1="75" y1="50" x2="75" y2="25"/>
        
        {/* Three open white circles at correct positions */}
        <circle cx="25" cy="75" r="5" fill="white" stroke="#007FFF" strokeWidth="3"/>  {/* Starting point */}
        <circle cx="50" cy="50" r="5" fill="white" stroke="#007FFF" strokeWidth="3"/>  {/* Turn from UP to RIGHT */}
        <circle cx="75" cy="25" r="5" fill="white" stroke="#007FFF" strokeWidth="3"/>  {/* End of final vertical line */}
      </g>
    </svg>
  );
} 