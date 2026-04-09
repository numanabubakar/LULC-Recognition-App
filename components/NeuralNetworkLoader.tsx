'use client';

export function NeuralNetworkLoader() {
  return (
    <div className="flex flex-col items-center justify-center gap-4 sm:gap-6 py-8 sm:py-12">
      {/* Neural Network Animation */}
      <div className="relative w-20 sm:w-24 h-20 sm:h-24">
        {/* Center node */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-6 h-6 rounded-full bg-gradient-to-br from-indigo-400 to-indigo-600 shadow-lg shadow-indigo-500/50 animate-pulse" />
        </div>

        {/* Orbiting nodes */}
        {[0, 1, 2, 3].map((i) => {
          const angle = (i * 90) * (Math.PI / 180);
          const radius = 40;
          const x = Math.cos(angle) * radius;
          const y = Math.sin(angle) * radius;

          return (
            <div
              key={i}
              className="absolute w-3 h-3 rounded-full bg-indigo-400 shadow-md shadow-indigo-400/50"
              style={{
                left: `calc(50% + ${x}px)`,
                top: `calc(50% + ${y}px)`,
                transform: 'translate(-50%, -50%)',
                animation: `spin 3s linear infinite`,
                animationDelay: `${i * 0.75}s`,
              }}
            />
          );
        })}

        {/* Connecting lines animation */}
        <svg
          className="absolute inset-0 w-full h-full"
          style={{ filter: 'drop-shadow(0 0 2px rgba(99, 102, 241, 0.3))' }}
        >
          <g stroke="rgba(99, 102, 241, 0.4)" strokeWidth="1" fill="none">
            {[0, 1, 2, 3].map((i) => {
              const angle = (i * 90) * (Math.PI / 180);
              const radius = 40;
              const x = Math.cos(angle) * radius;
              const y = Math.sin(angle) * radius;

              return (
                <line
                  key={i}
                  x1="50%"
                  y1="50%"
                  x2={`calc(50% + ${x}px)`}
                  y2={`calc(50% + ${y}px)`}
                  style={{
                    animation: `pulse 2s ease-in-out infinite`,
                    animationDelay: `${i * 0.5}s`,
                  }}
                  vectorEffect="non-scaling-stroke"
                />
              );
            })}
          </g>
        </svg>
      </div>

      {/* Status text */}
      <div className="text-center">
        <p className="text-xs sm:text-sm font-semibold text-slate-200">
          Processing Image
        </p>
        <p className="text-xs text-slate-400 mt-1">
          Running neural network inference...
        </p>
      </div>

      {/* Pixel processing animation */}
      <div className="flex gap-1">
        {[0, 1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className="w-2 h-2 rounded-full bg-indigo-500"
            style={{
              animation: `bounce 1.4s ease-in-out infinite`,
              animationDelay: `${i * 0.2}s`,
            }}
          />
        ))}
      </div>

      <style>{`
        @keyframes spin {
          from { transform: translate(-50%, -50%) rotate(0deg); }
          to { transform: translate(-50%, -50%) rotate(360deg); }
        }
        @keyframes bounce {
          0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
          40% { opacity: 1; transform: scale(1.2); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}
