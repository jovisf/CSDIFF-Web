'use client';
<<<<<<< HEAD
import React, { useState, useEffect } from 'react';
import { Zap, CheckCircle, Clock, Check } from 'lucide-react';;

=======
import { Zap, Clock, CheckCircle } from 'lucide-react';
import React, { useState } from 'react';
>>>>>>> origin/main
interface LoadingOptimizerProps {
  className?: string;
}

const LoadingOptimizer: React.FC<LoadingOptimizerProps> = ({
  className = ''
}) => {
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optimizations, setOptimizations] = useState<string[]>([]);
  const [completedOptimizations, setCompletedOptimizations] = useState<string[]>([]);

  const optimizationSteps = [
    'Analyzing bundle size...',
    'Optimizing images...',
    'Minifying CSS and JavaScript...',
    'Enabling compression...',
    'Setting up caching...',
    'Implementing lazy loading...',
    'Configuring CDN...',
    'Optimizing database queries...',
    'Enabling service worker...',
    'Finalizing optimizations...'
  ];

  const runOptimizations = async () => {
    setIsOptimizing(true);
    setOptimizations([]);
    setCompletedOptimizations([]);

    for (let i = 0; i < optimizationSteps.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 800));
      
      setOptimizations(prev => [...prev, optimizationSteps[i]]);
      
      // Mark as completed after a short delay
      setTimeout(() => {
        setCompletedOptimizations(prev => [...prev, optimizationSteps[i]]);
      }, 400);
    }

    setIsOptimizing(false);
  };

  return (
    <div className={`bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 ${className}`}>
      <div className="text-center mb-6">
        <Zap className="w-12 h-12 text-cyan-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-white mb-2">Loading Optimizer</h3>
        <p className="text-gray-300">Optimize your application's loading performance</p>
      </div>

      <div className="space-y-4">
        {/* Start Button */}
        <button
          onClick={runOptimizations}
          disabled={isOptimizing}
          className="w-full bg-gradient-to-r from-cyan-500 to-purple-600 text-white py-3 rounded-lg font-semibold hover:from-cyan-600 hover:to-purple-700 transition-all duration-300 flex items-center justify-center disabled:opacity-50"
        >
          {isOptimizing ? (
            <>
              <Clock className="w-5 h-5 mr-2 animate-spin" />
              Optimizing...
            </>
          ) : (
            <>
              <Zap className="w-5 h-5 mr-2" />
              Start Optimization
            </>
          )}
        </button>

        {/* Progress Bar */}
        {isOptimizing && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-400">
              <span>Progress</span>
              <span>{optimizations.length} / {optimizationSteps.length}</span>
            </div>
            <div className="w-full bg-slate-700 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-cyan-500 to-purple-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${(optimizations.length / optimizationSteps.length) * 100}%` }}
              />
            </div>
          </div>
        )}

        {/* Optimization Steps */}
        {optimizations.length > 0 && (
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {optimizationSteps.map((step, index) => {
              const isCompleted = completedOptimizations.includes(step);
              const isCurrent = optimizations.includes(step) && !isCompleted;
              
              return (
                <div
                  key={index}
                  className={`flex items-center space-x-3 p-2 rounded-lg transition-all duration-300 ${
                    isCompleted 
                      ? 'bg-green-500/10 border border-green-500/20' 
                      : isCurrent 
                        ? 'bg-cyan-500/10 border border-cyan-500/20' 
                        : 'bg-slate-700/30'
                  }`}
                >
                  {isCompleted ? (
                    <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0" />
                  ) : isCurrent ? (
                    <Clock className="w-5 h-5 text-cyan-400 flex-shrink-0 animate-spin" />
                  ) : (
                    <div className="w-5 h-5 rounded-full border-2 border-slate-500 flex-shrink-0" />
                  )}
                  <span className={`text-sm ${
                    isCompleted 
                      ? 'text-green-300' 
                      : isCurrent 
                        ? 'text-cyan-300' 
                        : 'text-gray-400'
                  }`}>
                    {step}
                  </span>
                </div>
              );
            })}
          </div>
        )}

        {/* Completion Message */}
        {!isOptimizing && completedOptimizations.length === optimizationSteps.length && (
          <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4 text-center">
            <CheckCircle className="w-8 h-8 text-green-400 mx-auto mb-2" />
            <h4 className="text-lg font-semibold text-green-300 mb-1">
              Optimization Complete!
            </h4>
            <p className="text-green-200 text-sm">
              Your application has been optimized for better performance.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default LoadingOptimizer;