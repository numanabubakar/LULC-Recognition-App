'use client';

export function TechnicalSpecs() {
  const specs = [
    {
      label: 'Architecture',
      value: 'AMFRNet',
      details: 'Convolutional Neural Network with interpretability features',
    },
    {
      label: 'Parameters',
      value: '~365K',
      details: 'Total trainable parameters in the model',
    },
    {
      label: 'FLOPs',
      value: '~106M',
      details: 'Floating point operations per inference',
    },
    {
      label: 'Input Size',
      value: '224×224',
      details: 'Standard remote sensing image resolution',
    },
    {
      label: 'Normalization',
      value: 'ImageNet',
      details: 'RGB normalization (μ=[0.485, 0.456, 0.406], σ=[0.229, 0.224, 0.225])',
    },
  ];

  return (
    <div className="w-full border-t border-slate-700 pt-6 sm:pt-8">
      <p className="text-xs uppercase tracking-wider text-slate-400 mb-4 sm:mb-6">
        Technical Specifications
      </p>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2 sm:gap-4">
        {specs.map((spec) => (
          <div
            key={spec.label}
            className="p-2.5 sm:p-3 rounded-lg bg-slate-800/50 border border-slate-700 hover:border-indigo-600/50 transition-colors"
            title={spec.details}
          >
            <p className="text-xs text-slate-400 mb-1 truncate">{spec.label}</p>
            <p className="font-semibold text-indigo-300 text-xs sm:text-sm truncate">{spec.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
