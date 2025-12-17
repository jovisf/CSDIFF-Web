'use client';
import React from 'react';
import Link from 'next/link';
import { Home, ArrowLeft, Search, AlertTriangle } from 'lucide-react';

const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center px-4">
      <div className="max-w-md w-full text-center">
        <div className="mb-8">
          <AlertTriangle className="w-24 h-24 text-red-400 mx-auto mb-6" />
          <h1 className="text-6xl font-bold text-white mb-4">404</h1>
          <h2 className="text-2xl font-semibold text-gray-300 mb-4">
            Page Not Found
          </h2>
          <p className="text-gray-400 mb-8">
            The page you're looking for doesn't exist or has been moved.
          </p>
        </div>

        <div className="space-y-4">
          <Link
            href="/"
            className="inline-flex items-center justify-center space-x-2 bg-gradient-to-r from-cyan-500 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-cyan-600 hover:to-purple-700 transition-all duration-300"
          >
            <Home className="w-5 h-5" />
            <span>Go Home</span>
          </Link>

          <button
            onClick={() => window.history.back()}
            className="inline-flex items-center justify-center space-x-2 border border-cyan-400 text-cyan-400 hover:bg-cyan-400 hover:text-white px-6 py-3 rounded-lg font-semibold transition-all duration-300 ml-4"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Go Back</span>
          </button>
        </div>

        <div className="mt-12">
          <p className="text-gray-500 text-sm mb-4">Or try searching:</p>
          <div className="relative">
            <input
              type="text"
              placeholder="Search for something..."
              className="w-full px-4 py-3 pl-10 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            />
            <Search className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
          </div>
        </div>

        <div className="mt-8 text-center">
          <p className="text-gray-500 text-sm">
            Need help? <Link href="/contact" className="text-cyan-400 hover:text-cyan-300">Contact us</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;