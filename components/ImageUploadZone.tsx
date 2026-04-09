'use client';

import { useState, useRef } from 'react';
import { Upload, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Image from 'next/image';

interface ImageUploadZoneProps {
  onImageSelected: (file: File, preview: string) => void;
  disabled?: boolean;
}

export function ImageUploadZone({
  onImageSelected,
  disabled = false,
}: ImageUploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      processFile(files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files;
    if (files && files.length > 0) {
      processFile(files[0]);
    }
  };

  const processFile = (file: File) => {
    // Validate file type
    if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
      alert('Please upload a JPEG or PNG image');
      return;
    }

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const previewUrl = e.target?.result as string;
      setPreview(previewUrl);
      setFileName(file.name);
      onImageSelected(file, previewUrl);
    };
    reader.readAsDataURL(file);
  };

  const clearImage = () => {
    setPreview(null);
    setFileName(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="w-full">
      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/png,image/jpg"
        onChange={handleFileSelect}
        disabled={disabled}
        className="hidden"
      />

      {!preview ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => !disabled && fileInputRef.current?.click()}
          className={`relative border-2 border-dashed rounded-lg sm:rounded-xl p-6 sm:p-8 transition-all duration-200 cursor-pointer ${
            isDragging
              ? 'border-indigo-500 bg-indigo-500/10'
              : 'border-slate-600 bg-slate-800/50 hover:border-indigo-400 hover:bg-indigo-500/5'
          } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <div className="flex flex-col items-center justify-center gap-3">
            <div className="p-2 sm:p-3 rounded-lg bg-indigo-600/20">
              <Upload className="w-5 sm:w-6 h-5 sm:h-6 text-indigo-400" />
            </div>
            <div className="text-center">
              <p className="text-xs sm:text-sm font-semibold text-slate-200">
                Drag and drop your image here
              </p>
              <p className="text-xs text-slate-400 mt-1">
                or click to select from your computer
              </p>
            </div>
            <p className="text-xs text-slate-500">
              Supported formats: JPEG, PNG
            </p>
          </div>
        </div>
      ) : (
        <div className="relative mx-auto w-full max-w-sm rounded-lg sm:rounded-xl overflow-hidden border border-indigo-600/50 bg-slate-800">
          <div className="relative h-56 sm:h-64 w-full">
            <Image
              src={preview}
              alt="Preview"
              fill
              className="object-contain"
            />
          </div>
          <div className="absolute top-2 right-2 flex gap-2">
            <button
              onClick={clearImage}
              disabled={disabled}
              className="p-1.5 sm:p-2 rounded-lg bg-slate-900/90 hover:bg-slate-800 text-slate-300 hover:text-red-400 transition-colors"
              title="Clear image"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <div className="p-2 sm:p-3 bg-slate-900/50 border-t border-slate-700">
            <p className="text-xs text-slate-400 truncate">
              {fileName}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
