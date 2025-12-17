import React, { useState, useEffect } from 'react';

interface PerformanceMetrics {
  renderTime: number;
  memoryUsage: number;
  fps: number;
}

const PerformanceDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<PerformanceMetrics>({
    renderTime: 0,
    memoryUsage: 0,
    fps: 0
  });

  useEffect(() => {
    let _frameCount = 0;
    let lastTime = performance.now();

    const updateMetrics = () => {
      const currentTime = performance.now();
      const renderTime = currentTime - lastTime;
      
      const memoryUsage = (performance as Performance & { memory?: { usedJSHeapSize: number } }).memory?.usedJSHeapSize || 0;
      
      _frameCount++;
      const fps = Math.round(1000 / renderTime);
      
      setMetrics({
        renderTime: Math.round(renderTime * 100) / 100,
        memoryUsage: Math.round(memoryUsage / 1024 / 1024 * 100) / 100,
        fps
      });
      
      lastTime = currentTime;
    };

    const interval: NodeJS.Timeout = setInterval(updateMetrics, 1000);

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, []);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Performance Dashboard</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-blue-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">Render Time</h3>
          <p className="text-3xl font-bold text-blue-600">{metrics.renderTime}ms</p>
        </div>
        
        <div className="bg-green-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-green-900 mb-2">Memory Usage</h3>
          <p className="text-3xl font-bold text-green-600">{metrics.memoryUsage}MB</p>
        </div>
        
        <div className="bg-purple-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-purple-900 mb-2">FPS</h3>
          <p className="text-3xl font-bold text-purple-600">{metrics.fps}</p>
        </div>
      </div>
    </div>
  );
};

export default PerformanceDashboard;