'use client';

import { Card } from '@/components/ui/card';
import { CheckCircle } from 'lucide-react';

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

interface PredictionResultsProps {
  result: PredictionResult;
}

export function PredictionResults({ result }: PredictionResultsProps) {
  const confidencePercent = Math.round(result.confidence * 100);
  const modelDisplayName = result.model_type.toUpperCase();

  return (
    <div className="w-full space-y-4">
      {/* Main Result Card */}
      <Card className="bg-slate-800 border-slate-700 p-4 sm:p-6">
        <div className="flex items-start gap-3 sm:gap-4">
          <div className="p-2 sm:p-3 rounded-lg bg-green-600/20 flex-shrink-0">
            <CheckCircle className="w-5 sm:w-6 h-5 sm:h-6 text-green-400" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs uppercase tracking-wider text-slate-400 mb-1">
              Prediction
            </p>
            <h3 className="text-xl sm:text-2xl font-bold text-white mb-2 break-words">
              {result.predicted_class}
            </h3>
            <p className="text-xs sm:text-sm text-slate-400 break-all">
              Class Index: <span className="text-indigo-300 font-mono">{result.class_index}</span>
            </p>
          </div>
        </div>
      </Card>

      {/* Confidence Gauge */}
      <Card className="bg-slate-800 border-slate-700 p-4 sm:p-6">
        <div className="space-y-4">
          <div>
            <p className="text-xs uppercase tracking-wider text-slate-400 mb-2">
              Confidence Score
            </p>
            <p className="text-2xl sm:text-3xl font-bold text-indigo-400">{confidencePercent}%</p>
          </div>

          {/* Radial Progress Bar */}
          <div className="flex items-center justify-center py-3 sm:py-4">
            <svg className="w-24 sm:w-32 h-24 sm:h-32 transform -rotate-90" viewBox="0 0 120 120">
              {/* Background circle */}
              <circle
                cx="60"
                cy="60"
                r="55"
                fill="none"
                stroke="rgba(51, 65, 85, 0.5)"
                strokeWidth="8"
              />
              {/* Progress circle */}
              <circle
                cx="60"
                cy="60"
                r="55"
                fill="none"
                stroke="url(#progressGradient)"
                strokeWidth="8"
                strokeDasharray={`${(confidencePercent / 100) * 345} 345`}
                strokeLinecap="round"
                className="transition-all duration-500"
              />
              {/* Gradient definition */}
              <defs>
                <linearGradient
                  id="progressGradient"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="100%"
                >
                  <stop offset="0%" stopColor="#6366f1" />
                  <stop offset="100%" stopColor="#818cf8" />
                </linearGradient>
              </defs>
            </svg>
          </div>

          {/* Linear Progress Bar */}
          <div className="space-y-2">
            <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-indigo-500 to-indigo-400 transition-all duration-500"
                style={{ width: `${confidencePercent}%` }}
              />
            </div>
            <p className="text-xs text-slate-500 text-right">
              {result.confidence.toFixed(4)}
            </p>
          </div>
        </div>
      </Card>

      {/* Visual Explanations (XAI) */}
      {result.explainability_maps && Object.keys(result.explainability_maps).length > 0 && (
        <Card className="bg-slate-800 border-slate-700 p-4 sm:p-6">
          <p className="text-xs uppercase tracking-wider text-slate-400 mb-4">
            Visual Explanations (XAI Maps)
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(result.explainability_maps).map(([mapName, b64Str]) => (
              <div key={mapName} className="rounded-lg bg-slate-900 border border-slate-800 overflow-hidden">
                <div className="bg-slate-800 px-3 py-2 border-b border-slate-700">
                  <p className="text-sm font-medium text-slate-300">{mapName}</p>
                </div>
                <div className="p-2 flex items-center justify-center bg-slate-950">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={b64Str}
                    alt={`${mapName} heatmap`}
                    className="w-full h-auto max-w-[224px] max-h-[224px] object-contain rounded"
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* All Predictions */}
      {result.all_predictions && result.all_predictions.length > 0 && (
        <Card className="bg-slate-800 border-slate-700 p-4 sm:p-6">
          <p className="text-xs uppercase tracking-wider text-slate-400 mb-4">
            All Class Probabilities
          </p>
          <div className="max-h-64 overflow-y-auto pr-2 space-y-3 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-slate-800/50">
            {result.all_predictions.map((pred, idx) => (
              <div key={pred.class_index} className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <span className="text-xs font-mono text-slate-500 w-4 text-right">{idx + 1}.</span>
                  <span className={`text-sm truncate ${idx === 0 ? 'text-indigo-300 font-semibold' : 'text-slate-300'}`}>
                    {pred.class_label}
                  </span>
                </div>
                <div className="flex items-center gap-3 w-1/3 sm:w-1/2">
                  <div className="hidden sm:block w-full h-1.5 bg-slate-700 rounded-full overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-500 ${idx === 0 ? 'bg-indigo-500' : 'bg-slate-500'}`}
                      style={{ width: `${pred.confidence * 100}%` }}
                    />
                  </div>
                  <span className={`text-xs font-mono w-12 text-right ${idx === 0 ? 'text-indigo-400 font-medium' : 'text-slate-400'}`}>
                    {(pred.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Performance Metrics */}
      <Card className="bg-slate-800 border-slate-700 p-4 sm:p-6">
        <p className="text-xs uppercase tracking-wider text-slate-400 mb-4">
          Performance Metrics
        </p>
        <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-4">
          <div className="p-2.5 sm:p-3 rounded-lg bg-slate-700/50 border border-slate-600">
            <p className="text-xs text-slate-400">Inference Time</p>
            <p className="text-sm sm:text-lg font-semibold text-indigo-300 mt-1 truncate">
              {result.inference_time_ms.toFixed(2)}ms
            </p>
          </div>
          <div className="p-2.5 sm:p-3 rounded-lg bg-slate-700/50 border border-slate-600">
            <p className="text-xs text-slate-400">Model</p>
            <p className="text-sm sm:text-lg font-semibold text-indigo-300 mt-1 truncate">
              {modelDisplayName}
            </p>
          </div>
          <div className="p-2.5 sm:p-3 rounded-lg bg-slate-700/50 border border-slate-600">
            <p className="text-xs text-slate-400">Image Size</p>
            <p className="text-xs sm:text-sm font-mono text-slate-300 mt-1 truncate">
              {result.image_info.width}×{result.image_info.height}
            </p>
          </div>
          <div className="p-2.5 sm:p-3 rounded-lg bg-slate-700/50 border border-slate-600">
            <p className="text-xs text-slate-400">Format</p>
            <p className="text-sm sm:text-lg font-semibold text-slate-300 mt-1 truncate">
              {result.image_info.format}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
