'use client';

import { useState } from 'react';
import { DatasetSelector, type DatasetType } from '@/components/DatasetSelector';
import { ImageUploadZone } from '@/components/ImageUploadZone';
import { NeuralNetworkLoader } from '@/components/NeuralNetworkLoader';
import { PredictionResults } from '@/components/PredictionResults';
import { TechnicalSpecs } from '@/components/TechnicalSpecs';
import { Card } from '@/components/ui/card';
import { Brain } from 'lucide-react';

interface ClassPrediction {
  class_index: number;
  class_label: string;
  confidence: number;
}

interface PredictionResult {
  predicted_class: string;
  class_index: number;
  confidence: number;
  all_predictions: ClassPrediction[];
  explainability_maps?: Record<string, string>;
  inference_time_ms: number;
  model_type: string;
  image_info: {
    width: number;
    height: number;
    format: string;
  };
}

export default function Dashboard() {
  const [selectedDataset, setSelectedDataset] = useState<DatasetType>('eurosat');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [uploadKey, setUploadKey] = useState(0);

  const handleImageSelected = (file: File, previewUrl: string) => {
    setSelectedFile(file);
    setPreview(previewUrl);
    setResult(null);
    setError(null);
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      setError('Please upload an image first');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('model_type', selectedDataset);

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      const response = await fetch(`${apiUrl}/predict`, {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'An error occurred during prediction';
      setError(errorMessage);
      console.error('[LULC] Prediction error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
          <div className="flex items-center justify-center gap-2 sm:gap-3 mb-1 sm:mb-2">
            <div className="p-2 rounded-lg bg-indigo-600/20">
              <Brain className="w-5 sm:w-6 h-5 sm:h-6 text-indigo-400" />
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white">LULC Recognition</h1>
          </div>
          <p className="text-center text-xs sm:text-sm text-slate-400">
            Deep Learning Land Use & Land Cover Classification System
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-6">

        {/* Upload & Select Card */}
        <Card className="bg-slate-900 border-slate-800 p-4 sm:p-6 space-y-6">
          <div>
            <p className="text-xs uppercase tracking-wider text-slate-400 mb-4">
              Image Input
            </p>
            <ImageUploadZone
              key={uploadKey}
              onImageSelected={handleImageSelected}
              disabled={isLoading}
            />
          </div>
          <div>
            <DatasetSelector
              selectedDataset={selectedDataset}
              onDatasetChange={setSelectedDataset}
            />
          </div>
        </Card>

        {/* Action Button */}
        {preview && !result && (
          <div className="flex gap-2 sm:gap-3">
            <button
              onClick={handlePredict}
              disabled={isLoading}
              className="flex-1 px-4 sm:px-6 py-2.5 sm:py-3 rounded-lg bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-700 text-white text-sm sm:text-base font-semibold transition-colors duration-200 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Processing...' : 'Run Inference'}
            </button>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <Card className="bg-slate-900 border-slate-800 p-6 sm:p-8">
            <NeuralNetworkLoader />
          </Card>
        )}

        {/* Error State */}
        {error && (
          <Card className="bg-red-900/20 border-red-700/50 p-4">
            <p className="text-sm text-red-300">{error}</p>
          </Card>
        )}

        {/* Results Section */}
        {result && !isLoading && (
          <div className="space-y-6">
            <PredictionResults result={result} />

            {/* Clear and Re-upload */}
            <div className="flex gap-2 sm:gap-3">
              <button
                onClick={() => {
                  setSelectedFile(null);
                  setPreview(null);
                  setResult(null);
                  setError(null);
                  setUploadKey(prev => prev + 1);
                }}
                className="flex-1 px-4 sm:px-6 py-2.5 sm:py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-sm sm:text-base font-semibold transition-colors duration-200 border border-slate-700"
              >
                Upload Another Image
              </button>
            </div>
          </div>
        )}

        {/* Technical Specs Footer */}
        {(preview || result) && (
          <TechnicalSpecs />
        )}

        {/* Info Panel */}
        {!preview && (
          <div className="mt-12 p-6 rounded-xl bg-slate-900 border border-slate-800">
            <h2 className="text-lg font-semibold text-white mb-4">
              Getting Started
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <h3 className="text-sm font-semibold text-indigo-400 mb-2">
                  1. Select Dataset
                </h3>
                <p className="text-sm text-slate-400">
                  Choose from EuroSAT, MLRSNet, or PatternNet benchmark datasets.
                </p>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-indigo-400 mb-2">
                  2. Upload Image
                </h3>
                <p className="text-sm text-slate-400">
                  Drag and drop or click to upload a JPEG or PNG satellite/aerial image.
                </p>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-indigo-400 mb-2">
                  3. Get Prediction
                </h3>
                <p className="text-sm text-slate-400">
                  Click "Run Inference" to classify the land use/cover with confidence scores.
                </p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 mt-12 py-6 text-center text-xs text-slate-500">
        <p>
          LULC Recognition System By Khadijah Shabbir & Numan Abubakar
        </p>
      </footer>
    </div>
  );
}
