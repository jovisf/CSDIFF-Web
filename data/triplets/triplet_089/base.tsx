'use client';
import React from 'react';
<<<<<<< HEAD
import { ArrowRight, CheckCircle, Star, Check } from 'lucide-react';;
=======
import { ArrowRight, CheckCircle, Star, } from 'lucide-react';
>>>>>>> origin/main
import Link from 'next/link';

interface GenericServicePageProps {
  title: string;
  description: string;
  features?: string[];
  benefits?: string[];
  pricing?: {
    basic: number;
    pro: number;
    enterprise: number;
  };
  className?: string;
}

const GenericServicePage: React.FC<GenericServicePageProps> = ({
  title,
  description,
  features = [],
  benefits = [],
  pricing,
  className = ''
}) => {
  return (
    <div className={`min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-20 ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            {title}
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            {description}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/contact"
              className="bg-gradient-to-r from-cyan-500 to-purple-600 text-white px-8 py-4 rounded-lg font-semibold hover:from-cyan-600 hover:to-purple-700 transition-all duration-300 flex items-center justify-center mx-auto w-fit"
            >
              Contact Us
              <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
            <button className="border border-cyan-400 text-cyan-400 hover:bg-cyan-400 hover:text-white px-8 py-4 rounded-lg font-semibold transition-all duration-300">
              Learn More
            </button>
          </div>
        </div>

        {/* Features Section */}
        {features.length > 0 && (
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-white text-center mb-12">Key Features</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature, index) => (
                <div key={index} className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 hover:border-cyan-400/50 transition-all duration-300">
                  <CheckCircle className="w-8 h-8 text-cyan-400 mb-4" />
                  <h3 className="text-lg font-semibold text-white mb-2">{feature}</h3>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Benefits Section */}
        {benefits.length > 0 && (
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-white text-center mb-12">Benefits</h2>
            <div className="grid md:grid-cols-2 gap-6">
              {benefits.map((benefit, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <Star className="w-6 h-6 text-cyan-400 mt-1 flex-shrink-0" />
                  <p className="text-gray-300 text-lg">{benefit}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Pricing Section */}
        {pricing && (
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-white text-center mb-12">Pricing</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-8 text-center">
                <h3 className="text-xl font-semibold text-white mb-4">Basic</h3>
                <div className="text-4xl font-bold text-cyan-400 mb-6">${pricing.basic}</div>
                <p className="text-gray-300 mb-6">Perfect for small businesses</p>
                <button className="w-full bg-slate-700 text-white py-3 rounded-lg hover:bg-slate-600 transition-colors">
                  Get Started
                </button>
              </div>
              <div className="bg-slate-800/50 backdrop-blur-sm border border-cyan-400 rounded-xl p-8 text-center relative">
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-cyan-400 text-slate-900 px-4 py-1 rounded-full text-sm font-semibold">
                  Most Popular
                </div>
                <h3 className="text-xl font-semibold text-white mb-4">Pro</h3>
                <div className="text-4xl font-bold text-cyan-400 mb-6">${pricing.pro}</div>
                <p className="text-gray-300 mb-6">Ideal for growing companies</p>
                <button className="w-full bg-cyan-600 text-white py-3 rounded-lg hover:bg-cyan-700 transition-colors">
                  Get Started
                </button>
              </div>
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-8 text-center">
                <h3 className="text-xl font-semibold text-white mb-4">Enterprise</h3>
                <div className="text-4xl font-bold text-cyan-400 mb-6">${pricing.enterprise}</div>
                <p className="text-gray-300 mb-6">For large organizations</p>
                <button className="w-full bg-slate-700 text-white py-3 rounded-lg hover:bg-slate-600 transition-colors">
                  Contact Sales
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GenericServicePage;