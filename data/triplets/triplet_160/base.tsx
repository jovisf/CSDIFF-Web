'use client';
<<<<<<< HEAD
import { ArrowRight, CheckCircle, Check } from 'lucide-react';;
=======

import { ArrowRight, CheckCircle, } from 'lucide-react';
>>>>>>> origin/main
import Navigation from '../components/Navigation';
import Footer from '../components/Footer';

const stats = [
  { number: '1B+', label: 'People with disabilities worldwide' },
  { number: '15%', label: 'Of global population' },
  { number: '$13T', label: 'Annual spending power' },
  { number: '71%', label: 'Leave sites due to accessibility issues' }
];

const features = [
  {
    title: 'AI-Powered Audits',
    description: 'Automated accessibility testing using advanced AI algorithms to identify issues quickly and accurately.',
    icon: 'ai-audit',
    benefits: [
      'Comprehensive WCAG 2.1 AA compliance checking',
      'Real-time issue detection and reporting',
      'Automated remediation suggestions',
      'Detailed accessibility score and recommendations'
    ]
  },
  {
    title: 'Manual Testing',
    description: 'Expert human testing to catch issues that automated tools might miss.',
    icon: 'manual-test',
    benefits: [
      'Screen reader compatibility testing',
      'Keyboard navigation verification',
      'Color contrast and visual accessibility',
      'User experience evaluation'
    ]
  }
];

const services = [
  {
    title: 'Accessibility Audit',
    description: 'Comprehensive evaluation of your digital assets',
    price: 'Starting at $500'
  },
  {
    title: 'Implementation',
    description: 'Fix identified accessibility issues',
    price: 'Starting at $1,000'
  },
  {
    title: 'Training',
    description: 'Team training on accessibility best practices',
    price: 'Starting at $300'
  },
  {
    title: 'Ongoing Support',
    description: 'Continuous monitoring and maintenance',
    price: 'Starting at $200/mo'
  }
];

export default function AccessibilityPage() {
  return (
    <>
      <Navigation />
      
      {/* Hero Section */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-600/20 to-blue-600/20"></div>
        <div className="relative max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            Accessibility Solutions
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Make your digital experiences inclusive and accessible to everyone. 
            Our AI-powered accessibility solutions ensure compliance and improve user experience for all.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="inline-flex items-center px-8 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-semibold">
              Get Accessibility Audit
              <ArrowRight className="ml-2 h-5 w-5" />
            </button>
            <button className="inline-flex items-center px-8 py-3 border-2 border-white text-white rounded-lg hover:bg-white hover:text-emerald-600 transition-colors font-semibold">
              View Our Services
            </button>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">The Accessibility Challenge</h2>
            <p className="text-xl text-gray-600">
              Digital accessibility is not just a legal requirement—it's a business imperative.
            </p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl font-bold text-emerald-600 mb-2">{stat.number}</div>
                <div className="text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Accessibility Solutions</h2>
            <p className="text-xl text-gray-600">
              Comprehensive tools and services to make your digital assets accessible to everyone.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center mr-4">
<<<<<<< HEAD
                    <div className="h-6 w-6 bg-emerald-600 rounded" />
=======
                    {feature.icon()}
>>>>>>> origin/main
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">{feature.title}</h3>
                </div>
                <p className="text-gray-600 mb-6">{feature.description}</p>
                <ul className="space-y-2">
                  {feature.benefits.map((benefit, benefitIndex) => (
                    <li key={benefitIndex} className="flex items-center text-gray-700">
                      <CheckCircle className="h-4 w-4 text-emerald-500 mr-2" />
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Services</h2>
            <p className="text-xl text-gray-600">
              From audits to implementation, we provide end-to-end accessibility solutions.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {services.map((service, index) => (
              <div key={index} className="bg-white rounded-xl p-6 shadow-lg border border-gray-200 text-center">
                <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
<<<<<<< HEAD
                  <div className="h-8 w-8 bg-emerald-600 rounded" />
=======
                  {service.icon()}
>>>>>>> origin/main
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{service.title}</h3>
                <p className="text-gray-600 mb-4">{service.description}</p>
                <div className="text-2xl font-bold text-emerald-600">{service.price}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 bg-emerald-600">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Make Your Digital Assets Accessible?
          </h2>
          <p className="text-xl text-emerald-100 mb-8 max-w-2xl mx-auto">
            Let's work together to create inclusive digital experiences that work for everyone.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="inline-flex items-center px-8 py-3 bg-white text-emerald-600 rounded-lg hover:bg-gray-100 transition-colors font-semibold">
              Start Your Accessibility Journey
              <ArrowRight className="ml-2 h-5 w-5" />
            </button>
            <button className="inline-flex items-center px-8 py-3 border-2 border-white text-white rounded-lg hover:bg-white hover:text-emerald-600 transition-colors font-semibold">
              Schedule Consultation
            </button>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}