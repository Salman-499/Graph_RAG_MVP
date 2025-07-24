import StepwiseLogo from './StepwiseLogo';

export default function Footer() {
  return (
    <footer className="bg-gray-100 border-t border-gray-300 py-4 mt-8">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-center space-x-2 text-gray-500">
          <span className="text-sm font-light">Powered by</span>
          
          {/* Stepwise Labs Logo */}
          <div className="flex items-center space-x-0.2">
            <StepwiseLogo width={20} height={16} />
            
            <span className="text-sm font-semibold text-gray-700">Stepwise Labs</span>
          </div>
        </div>
      </div>
    </footer>
  );
} 