'use client';
import { Zap, Brain, Globe, Users, TrendingUp, Clock, Star, CheckCircle, Target, Shield, Database } from 'lucide-react';

import React, { useState, useEffect } from 'react';
<<<<<<< HEAD
import { CheckCircle, Zap, Check, Brain, Globe, Users, TrendingUp, Clock, Shield, Star, Target, Database } from 'lucide-react';;

=======
>>>>>>> origin/main
const ContentStatistics: React.FC = () => {
  const [counters, setCounters] = useState({
    clients: 0,
    projects: 0,
    satisfaction: 0,
    years: 0
  });

  useEffect(() => {
    const targetCounters = {
      clients: 1000,
      projects: 500,
      satisfaction: 99,
      years: 5
    };

    const duration = 2000; // 2 seconds
    const steps = 60;
    const stepDuration = duration / steps;

    const interval = setInterval(() => {
      setCounters(prev => {
        const newCounters = { ...prev };
        let allComplete = true;
        
        Object.keys(targetCounters).forEach(key => {
          const target = targetCounters[key as keyof typeof targetCounters];
          const current = prev[key as keyof typeof prev];
          const increment = target / steps;
          
          if (current < target) {
            newCounters[key as keyof typeof newCounters] = Math.min(
              current + increment,
              target
            );
            allComplete = false;
          }
        });
        
        if (allComplete) {
          clearInterval(interval);
        }
        
        return newCounters;
      });
    }, stepDuration);

    return () => clearInterval(interval);
  }, []);

  const statistics = [
    {
      icon: Users,
      value: Math.floor(counters.clients),
      label: 'Happy Clients',
      suffix: '+',
      color: 'text-blue-400',
      description: 'Businesses trust our solutions'
    },
    {
      icon: Target,
      value: Math.floor(counters.projects),
      label: 'Projects Completed',
      suffix: '+',
      color: 'text-purple-400',
      description: 'Successful implementations'
    },
    {
      icon: TrendingUp,
      value: Math.floor(counters.satisfaction),
      label: 'Client Satisfaction',
      suffix: '%',
      color: 'text-green-400',
      description: 'Customer satisfaction rate'
    },
    {
      icon: Clock,
      value: Math.floor(counters.years),
      label: 'Years Experience',
      suffix: '+',
      color: 'text-yellow-400',
      description: 'Industry expertise'
    }
  ];

  const achievements = [
    {
      icon: Star,
      title: 'Industry Recognition',
      description: 'Awarded Best AI Solutions Provider 2024',
      value: '25+'
    },
    {
      icon: Target,
      title: 'Success Rate',
      description: 'Projects delivered on time and within budget',
      value: '98%'
    },
    {
      icon: Zap,
      title: 'Growth Rate',
      description: 'Year-over-year business growth',
      value: '300%'
    }
  ];

  const features = [
    {
      icon: Brain,
      title: 'AI Innovation',
      description: 'Leading the industry in AI-powered solutions',
      stats: ['Advanced ML algorithms', 'Real-time processing', 'Predictive analytics']
    },
    {
      icon: Shield,
      title: 'Security Excellence',
      description: 'Bank-level security for all our solutions',
      stats: ['End-to-end encryption', 'GDPR compliance', 'SOC 2 certified']
    },
    {
      icon: Globe,
      title: 'Global Reach',
      description: 'Worldwide deployment and support',
      stats: ['50+ Countries', '15+ Languages', '24/7 Support']
    },
    {
      icon: Database,
      title: 'Scalable Solutions',
      description: 'Built to grow with your business',
      stats: ['Auto-scaling', 'Cloud-native', 'High availability']
    }
  ];

  const benefits = [
    'Advanced AI technology integration',
    'Real-time processing and analytics',
    'Enterprise-grade security and compliance',
    'Scalable and flexible solutions',
    '24/7 technical support',
    'Easy integration with existing systems',
    'Cost-effective pricing plans',
    'Proven track record of success'
  ];

  return (
    <div className="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Our <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">Impact</span> in Numbers
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            See how we've helped businesses transform with our AI and IT solutions.
          </p>
        </div>

        {/* Statistics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {statistics.map((stat, index) => (
            <div key={index} className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10 text-center hover:bg-white/10 transition-all duration-300">
              <div className="flex justify-center mb-4">
                <div className="bg-gradient-to-r from-purple-600 to-cyan-600 w-16 h-16 rounded-full flex items-center justify-center">
                  <stat.icon className="h-8 w-8 text-white" />
                </div>
              </div>
              <div className={`text-3xl font-bold ${stat.color} mb-2`}>
                {stat.value}{stat.suffix}
              </div>
              <div className="text-gray-300">{stat.label}</div>
              <div className="text-gray-400 text-sm mt-2">{stat.description}</div>
            </div>
          ))}
        </div>

        {/* Features Section */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-white mb-4">Key Features</h3>
            <p className="text-gray-300 max-w-2xl mx-auto">
              Discover the powerful features that make our solutions stand out.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white/5 backdrop-blur-sm rounded-xl p-6 hover:bg-white/10 transition-all duration-300">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h4 className="text-lg font-semibold text-white mb-3">{feature.title}</h4>
                <p className="text-gray-300 text-sm mb-4">{feature.description}</p>
                <div className="space-y-2">
                  {feature.stats.map((stat, statIndex) => (
                    <div key={statIndex} className="flex items-center text-gray-300 text-sm">
                      <CheckCircle className="w-4 h-4 text-green-400 mr-2 flex-shrink-0" />
                      <span>{stat}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Achievements Section */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-white mb-4">Our Achievements</h3>
            <p className="text-gray-300 max-w-2xl mx-auto">
              Recognition and milestones that showcase our commitment to excellence.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {achievements.map((achievement, index) => (
              <div key={index} className="bg-white/5 backdrop-blur-sm rounded-xl p-8 text-center hover:bg-white/10 transition-all duration-300">
                <div className="w-16 h-16 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <achievement.icon className="w-8 h-8 text-white" />
                </div>
                <div className="text-3xl font-bold text-white mb-2">{achievement.value}</div>
                <h4 className="text-lg font-semibold text-white mb-2">{achievement.title}</h4>
                <p className="text-gray-300 text-sm">{achievement.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Benefits Section */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-white mb-4">Why Choose Us?</h3>
            <p className="text-gray-300 max-w-2xl mx-auto">
              Discover the advantages that make our solutions the preferred choice.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {benefits.map((benefit, index) => (
              <div key={index} className="flex items-center gap-3 bg-white/5 backdrop-blur-sm rounded-lg p-4 hover:bg-white/10 transition-all duration-300">
                <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0" />
                <span className="text-gray-300">{benefit}</span>
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-12">
            <h3 className="text-3xl font-bold text-white mb-4">Ready to Get Started?</h3>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Join thousands of satisfied customers and transform your business today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-8 py-4 rounded-lg font-semibold hover:from-cyan-600 hover:to-blue-700 transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-2">
                <Zap className="w-5 h-5" />
                Get Started Today
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white/10 transition-colors duration-200">
                View Case Studies
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContentStatistics;
