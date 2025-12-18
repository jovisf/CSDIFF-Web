'use client';
import React, { useState, useCallback } from 'react';
<<<<<<< HEAD
import { Upload, Download, Zap, ImageIcon } from 'lucide-react';;
=======
import { Upload, Download, ImageIcon, Zap } from 'lucide-react';
>>>>>>> origin/main

interface ImageOptimizerProps {
  onImageOptimized?: (optimizedImage: File) => void;
  className?: string;
}

const ImageOptimizer: React.FC<ImageOptimizerProps> = ({
  onImageOptimized,
  className = ''
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [optimizedFile, setOptimizedFile] = useState<File | null>(null);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optimizationStats, setOptimizationStats] = useState<{
    originalSize: number;
    optimizedSize: number;
    compressionRatio: number;
  } | null>(null);

  const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setOptimizedFile(null);
      setOptimizationStats(null);
    }
  }, []);

  const optimizeImage = useCallback(async () => {
    if (!selectedFile) return;

    setIsOptimizing(true);
    
    try {
      // Simulate image optimization
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Create a mock optimized file (in real implementation, you'd use a library like sharp)
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new window.Image();
      
      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx?.drawImage(img, 0, 0);
        
        canvas.toBlob((blob) => {
          if (blob) {
            const optimizedFile = new File([blob], `optimized_${selectedFile.name}`, {
              type: 'image/jpeg',
              lastModified: Date.now()
            });
            
            setOptimizedFile(optimizedFile);
            
            const originalSize = selectedFile.size;
            const optimizedSize = optimizedFile.size;
            const compressionRatio = ((originalSize - optimizedSize) / originalSize) * 100;
            
            setOptimizationStats({
              originalSize,
              optimizedSize,
              compressionRatio
            });
            
            onImageOptimized?.(optimizedFile);
          }
        }, 'image/jpeg', 0.8);
      };
      
      img.src = URL.createObjectURL(selectedFile);
    } catch (error) {
      console.error('Error optimizing image:', error);
    } finally {
      setIsOptimizing(false);
    }
  }, [selectedFile, onImageOptimized]);

  const downloadOptimizedImage = useCallback(() => {
    if (optimizedFile) {
      const url = URL.createObjectURL(optimizedFile);
      const a = document.createElement('a');
      a.href = url;
      a.download = optimizedFile.name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  }, [optimizedFile]);

  return (
    <div className={`bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 ${className}`}>
      <div className="text-center mb-6">
        <ImageIcon className="w-12 h-12 text-cyan-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-white mb-2">Image Optimizer</h3>
        <p className="text-gray-300">Optimize your images for better performance</p>
      </div>

      <div className="space-y-4">
        {/* File Upload */}
        <div className="border-2 border-dashed border-slate-600 rounded-lg p-6 text-center hover:border-cyan-400 transition-colors">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
            id="image-upload"
          />
          <label
            htmlFor="image-upload"
            className="cursor-pointer flex flex-col items-center space-y-2"
          >
            <Upload className="w-8 h-8 text-gray-400" />
            <span className="text-gray-300">
              {selectedFile ? selectedFile.name : 'Click to select an image'}
            </span>
          </label>
        </div>

        {/* Optimization Button */}
        {selectedFile && !optimizedFile && (
          <button
            onClick={optimizeImage}
            disabled={isOptimizing}
            className="w-full bg-gradient-to-r from-cyan-500 to-purple-600 text-white py-3 rounded-lg font-semibold hover:from-cyan-600 hover:to-purple-700 transition-all duration-300 flex items-center justify-center disabled:opacity-50"
          >
            {isOptimizing ? (
              <>
                <Zap className="w-5 h-5 mr-2 animate-spin" />
                Optimizing...
              </>
            ) : (
              <>
                <Zap className="w-5 h-5 mr-2" />
                Optimize Image
              </>
            )}
          </button>
        )}

        {/* Optimization Stats */}
        {optimizationStats && (
          <div className="bg-slate-700/50 rounded-lg p-4 space-y-2">
            <h4 className="text-lg font-semibold text-white mb-3">Optimization Results</h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-400">Original Size:</span>
                <span className="text-white ml-2">
                  {(optimizationStats.originalSize / 1024).toFixed(2)} KB
                </span>
              </div>
              <div>
                <span className="text-gray-400">Optimized Size:</span>
                <span className="text-white ml-2">
                  {(optimizationStats.optimizedSize / 1024).toFixed(2)} KB
                </span>
              </div>
              <div className="col-span-2">
                <span className="text-gray-400">Compression Ratio:</span>
                <span className="text-cyan-400 ml-2 font-semibold">
                  {optimizationStats.compressionRatio.toFixed(1)}% smaller
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Download Button */}
        {optimizedFile && (
          <button
            onClick={downloadOptimizedImage}
            className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold transition-colors duration-300 flex items-center justify-center"
          >
            <Download className="w-5 h-5 mr-2" />
            Download Optimized Image
          </button>
        )}
      </div>
    </div>
  );
};

export default ImageOptimizer;