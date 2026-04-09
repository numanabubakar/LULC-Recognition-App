'use client';

export type DatasetType = 'eurosat' | 'mlrsnet' | 'patternnet';

interface DatasetSelectorProps {
  selectedDataset: DatasetType;
  onDatasetChange: (dataset: DatasetType) => void;
}

export function DatasetSelector({
  selectedDataset,
  onDatasetChange,
}: DatasetSelectorProps) {
  const datasets = [
    {
      id: 'eurosat' as DatasetType,
      name: 'EuroSAT',
      classes: 10,
      description: 'European satellite imagery',
    },
    {
      id: 'mlrsnet' as DatasetType,
      name: 'MLRSNet',
      classes: 46,
      description: 'Multi-spectral remote sensing',
    },
    {
      id: 'patternnet' as DatasetType,
      name: 'PatternNet',
      classes: 38,
      description: 'High-resolution benchmark',
    },
  ];

  const selectedDesc = datasets.find(d => d.id === selectedDataset)?.description || '';

  return (
    <div className="w-full flex flex-col gap-2">
      <label className="text-xs uppercase tracking-wider text-slate-400">
        Benchmark Dataset
      </label>
      <select
        value={selectedDataset}
        onChange={(e) => onDatasetChange(e.target.value as DatasetType)}
        className="w-full p-2.5 sm:p-3 rounded-lg bg-slate-800 border border-slate-700 text-slate-200 outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all font-medium"
      >
        {datasets.map((dataset) => (
          <option key={dataset.id} value={dataset.id}>
            {dataset.name} - {dataset.classes} classes
          </option>
        ))}
      </select>
      <p className="text-xs text-slate-500">{selectedDesc}</p>
    </div>
  );
}
