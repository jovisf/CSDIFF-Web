'use client';
import { Zap, Brain, ArrowRight, CheckCircle, Play, Shield } from 'lucide-react';
import React, { useState } from 'react';
<<<<<<< HEAD
import { Play, CheckCircle, ArrowRight, Check, Zap, Brain, Shield } from 'lucide-react';;
=======
>>>>>>> origin/main
const DemoPage: React.FC = () => {
  const [activeDemo, setActiveDemo] = useState('ai-chatbot')
  const demos = [
    {
      id: 'ai-chatbot',
    title: 'AI Chatbot Demo',
      description: 'Experience our intelligent chatbot that can handle customer inquiries 24/7.',
    icon: Brain,
    features: ['Natural Language Processing', 'Context Awareness', 'Multi-language Support', 'Integration Ready']
  },
  {
    id: 'ai-automation',
    title: 'AI Automation Demo',
      description: 'See how AI can automate complex business processes and workflows.',
    icon: Zap,
    features: ['Workflow Automation', 'Smart Decision Making', 'Process Optimization', 'Real-time Monitoring']
  },
  {
    id: 'ai-security',
    title: 'AI Security Demo',
      description: 'Discover our AI-powered security solutions for threat detection and prevention.',
    icon: Shield,
    features: ['Threat Detection', 'Anomaly Detection', 'Automated Response', 'Security Analytics']
}
  ]
  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 pt-16">
        {/* Hero Section */}
        <section className="py-20">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-5xl md: text-6xl font-bold text-white mb-6">
              Interactive <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">Demos</span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Experience our AI and IT solutions firsthand. Try our interactive demos to see how our technology can transform your business.
            </p>
          </div>
        </section>
        {/* Demo Selection */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="grid grid-cols-1 md: grid-cols-3 gap-8 mb-12">
                {demos.map((demo) => (
                  <div
                    key={demo.id}
                    onClick={() => setActiveDemo(demo.id)}
                    className={`cursor-pointer p-6 rounded-lg transition-all duration-300 ${
                      activeDemo === demo.id
                        ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 border-2 border-cyan-400'
                        : 'bg-white/10 hover: bg-white/20 border-2 border-transparent'}`}
                  >
                    <div className="flex items-center mb-4">
                      <demo.icon className="w-8 h-8 text-cyan-400" />
                      <h3 className="text-xl font-bold text-white ml-3">{demo.title}</h3>
                    </div>
                    <p className="text-gray-300 mb-4">{demo.description}</p>
                    <ul className="space-y-2">
                      {demo.features.map((feature, index) => (
                        <li key={index} className="flex items-center text-sm text-gray-300">
                          <CheckCircle className="w-8 h-8" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
              {/* Demo Content */}
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold text-white mb-4">
                    {demos.find(d => d.id === activeDemo)?.title}
                  </h2>
                  <p className="text-gray-300">
                    {demos.find(d => d.id === activeDemo)?.description}
                  </p>
                </div>
                <div className="bg-black/50 rounded-lg p-8 mb-8">
                  <div className="flex items-center justify-center h-64 bg-gradient-to-br from-gray-800 to-gray-900 rounded-lg">
                    <div className="text-center">
                      <Play className="w-16 h-16 text-cyan-400 mx-auto mb-4" />
                      <h3 className="text-xl font-bold text-white mb-2">Demo Coming Soon</h3>
                      <p className="text-gray-400">
                        This interactive demo is currently under development. Contact us to schedule a live demonstration.
                      </p>
                    </div>
                  </div>
                </div>
                <div className="text-center">
                  <button className="bg-gradient-to-r from-cyan-500 to-purple-500 hover: from-cyan-600 hover:to-purple-600 text-white font-bold py-4 px-8 rounded-lg transition-all duration-300 flex items-center mx-auto">
                    Schedule Live Demo
                    <ArrowRight className="w-8 h-8" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
        {/* CTA Section */}
        <section className="py-20">
          <div className="container mx-auto px-4 text-center">
            <div className="bg-gradient-to-r from-cyan-500/20 to-purple-500/20 backdrop-blur-sm rounded-2xl p-12">
              <h2 className="text-4xl font-bold text-white mb-6">Ready to See More?</h2>
              <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
                Contact our team to schedule a personalized demonstration of our AI and IT solutions.
              </p>
              <div className="flex flex-col sm: flex-row gap-4 justify-center">
                <button className="bg-gradient-to-r from-cyan-500 to-purple-500 hover: from-cyan-600 hover:to-purple-600 text-white font-bold py-4 px-8 rounded-lg transition-all duration-300 transform hover:scale-105 flex items-center justify-center">
                  Contact Us
                  <ArrowRight className="w-8 h-8" />
                </button>
                <button className="border-2 border-white text-white hover: bg-white hover:text-gray-900 font-bold py-4 px-8 rounded-lg transition-all duration-300 flex items-center justify-center">
                  Learn More
                </button>
              </div>
            </div>
          </div>
        </section>
      </div>
</>
  )
}
export default DemoPage