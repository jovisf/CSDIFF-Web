'use client';
import { Zap, Brain, Settings, Globe, Users, BarChart, MessageCircle, Clock, ArrowRight, CheckCircle, Workflow, Target, ShoppingCart, Server } from 'lucide-react';
import React from 'react';
import Link from 'next/link';
<<<<<<< HEAD
import { ArrowRight, CheckCircle, Check, Zap, Brain, Settings, Globe, Users, BarChart, MessageCircle, Clock, Target, ShoppingCart, Server, Workflow } from 'lucide-react';;
=======
>>>>>>> origin/main
const AiChatbotBuilderPage: React.FC = () => {
  const features = [
    {
      title: 'No-Code Builder',
      description: 'Create sophisticated chatbots without any programming knowledge using our visual interface',
      icon: Zap,
      color: 'from-cyan-500 to-blue-500'
    },
    {
      title: 'Multi-Language Support',
      description: 'Deploy chatbots in 50+ languages with automatic translation and localization',
      icon: Globe,
      color: 'from-green-500 to-emerald-500'
    },
    {
      title: 'Advanced Analytics',
      description: 'Track performance with detailed analytics, conversation insights, and user behavior data',
      icon: BarChart,
      color: 'from-purple-500 to-pink-500'
    },
    {
      title: 'AI-Powered Responses',
      description: 'Leverage advanced NLP and machine learning for intelligent, context-aware conversations',
      icon: Brain,
      color: 'from-orange-500 to-red-500'
    },
    {
      title: 'Easy Integration',
      description: 'Seamlessly integrate with your existing systems, websites, and messaging platforms',
      icon: Workflow,
      color: 'from-blue-500 to-cyan-500'
    },
    {
      title: 'Custom Branding',
      description: 'Customize the chatbot appearance to match your brand identity and design guidelines',
      icon: Settings,
      color: 'from-indigo-500 to-purple-500'
    }
  ]
  const useCases = [
    {
      title: 'Customer Support',
      description: 'Provide 24/7 customer support with instant responses to common queries',
      icon: MessageCircle,
      benefits: ['Reduce support tickets by 60%', '24/7 availability', 'Instant responses']
    },
    {
      title: 'Lead Generation',
      description: 'Qualify leads and capture contact information through engaging conversations',
      icon: Target,
      benefits: ['Increase lead quality by 40%', 'Automated qualification', 'Higher conversion rates']
    },
    {
      title: 'E-commerce Assistant',
      description: 'Help customers find products, answer questions, and guide them through purchases',
      icon: ShoppingCart,
      benefits: ['Boost sales by 25%', 'Reduce cart abandonment', 'Personalized recommendations']
    },
    {
      title: 'Internal HR Bot',
      description: 'Answer employee questions about policies, benefits, and company information',
      icon: Users,
      benefits: ['Reduce HR workload', 'Consistent information', 'Employee satisfaction']
    }
  ]
  const pricing = [
    {
      name: 'Starter',
      price: '$29',
      period: '/month',
      description: 'Perfect for small businesses getting started',
      features: [
        'Up to 1,000 conversations/month',
        'Basic AI responses',
        'Email support',
        'Standard templates',
        'Basic analytics'
      ],
      popular: false
    },
    {
      name: 'Professional',
      price: '$99',
      period: '/month',
      description: 'Ideal for growing businesses with more needs',
      features: [
        'Up to 10,000 conversations/month',
        'Advanced AI with custom training',
        'Priority support',
        'Custom branding',
        'Advanced analytics',
        'Multi-language support',
        'API access'
      ],
      popular: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: '',
      description: 'For large organizations with complex requirements',
      features: [
        'Unlimited conversations',
        'Custom AI models',
        'Dedicated support',
        'White-label solution',
        'Advanced integrations',
        'Custom development',
        'SLA guarantee'
      ],
      popular: false
    }
  ]
  const stats = [
    { number: '10,000+', label: 'Chatbots Created', icon: MessageCircle },
    { number: '50+', label: 'Languages Supported', icon: Globe },
    { number: '99.9%', label: 'Uptime Guarantee', icon: Server },
    { number: '24/7', label: 'Customer Support', icon: Clock }
  ]
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm: px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md: text-6xl font-bold text-white mb-6">
            AI <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">Chatbot Builder</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Create intelligent, conversational chatbots without any coding knowledge. Our no-code platform makes it easy to build, deploy, and manage AI-powered chatbots for your business.
          </p>
          <div className="flex flex-col sm: flex-row gap-4 justify-center">
            <Link
              href="/contact"
              className="inline-flex items-center px-8 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-semibold rounded-lg hover:from-cyan-600 hover:to-purple-600 transition-all duration-300"
            >
              Start Building Free
              <ArrowRight className="w-8 h-8" />
            </Link>
            <Link
              href="/ai-services"
              className="inline-flex items-center px-8 py-3 border-2 border-cyan-400 text-cyan-400 font-semibold rounded-lg hover:bg-cyan-400 hover:text-white transition-all duration-300"
            >
              View All AI Services
            </Link>
          </div>
        </div>
      </section>
      {/* Stats Section */}
      <section className="py-16 px-4 sm: px-6 lg:px-8 bg-black/20">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md: grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full mb-4">
                  <stat.icon className="w-8 h-8 text-white" />
                </div>
                <div className="text-3xl font-bold text-white mb-2">{stat.number}</div>
                <div className="text-gray-300">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
      {/* Features Section */}
      <section className="py-20 px-4 sm: px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md: text-4xl font-bold text-white mb-6">
              Powerful Features for Every Business
            </h2>
            <p className="text-lg text-gray-300 max-w-3xl mx-auto">
              Our AI chatbot builder comes with everything you need to create sophisticated, intelligent chatbots that engage your customers and drive results.
            </p>
          </div>
          <div className="grid md: grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white/5 backdrop-blur-sm rounded-2xl p-8 border border-white/10 hover: border-cyan-400/50 transition-all duration-300 group">
                <div className="mb-6">
                  <feature.icon className="w-12 h-12 text-cyan-400" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-4">{feature.title}</h3>
                <p className="text-gray-300">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      {/* Use Cases Section */}
      <section className="py-20 px-4 sm: px-6 lg:px-8 bg-black/20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md: text-4xl font-bold text-white mb-6">
              Real-World Use Cases
            </h2>
            <p className="text-lg text-gray-300 max-w-3xl mx-auto">
              See how businesses across industries are using our chatbot builder to improve customer experience and drive growth.
            </p>
          </div>
          <div className="grid md: grid-cols-2 lg:grid-cols-4 gap-8">
            {useCases.map((useCase, index) => (
              <div key={index} className="bg-white/5 backdrop-blur-sm rounded-2xl p-8 border border-white/10 hover: border-purple-400/50 transition-all duration-300 group">
                <div className="mb-6">
                  <useCase.icon className="w-12 h-12 text-purple-400" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-4">{useCase.title}</h3>
                <p className="text-gray-300 mb-4">{useCase.description}</p>
                <ul className="space-y-2">
                  {useCase.benefits.map((benefit, idx) => (
                    <li key={idx} className="flex items-center text-sm text-gray-300">
                      <CheckCircle className="w-8 h-8" />
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>
      {/* Pricing Section */}
      <section className="py-20 px-4 sm: px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md: text-4xl font-bold text-white mb-6">
              Simple, Transparent Pricing
            </h2>
            <p className="text-lg text-gray-300 max-w-3xl mx-auto">
              Choose the plan that fits your business needs. All plans include our core features with no hidden fees.
            </p>
          </div>
          <div className="grid md: grid-cols-3 gap-8">
            {pricing.map((plan, index) => (
              <div key={index} className={`bg-white/5 backdrop-blur-sm rounded-2xl p-8 border transition-all duration-300 ${
                plan.popular
                  ? 'border-cyan-400/50 ring-2 ring-cyan-400/20'
                  : 'border-white/10 hover: border-cyan-400/50'}`}>
                {plan.popular && (
                  <div className="bg-gradient-to-r from-cyan-500 to-purple-500 text-white text-sm font-semibold px-4 py-2 rounded-full text-center mb-6">
                    Most Popular
                  </div>
                )}
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                  <div className="flex items-baseline justify-center mb-2">
                    <span className="text-4xl font-bold text-white">{plan.price}</span>
                    <span className="text-gray-300 ml-1">{plan.period}</span>
                  </div>
                  <p className="text-gray-300">{plan.description}</p>
                </div>
                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center">
                      <CheckCircle className="w-8 h-8" />
                      <span className="text-gray-300">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Link
                  href="/contact"
                  className={`w-full inline-flex items-center justify-center px-6 py-3 font-semibold rounded-lg transition-all duration-300 ${
                    plan.popular
                      ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white hover: from-cyan-600 hover:to-purple-600'
                      : 'border-2 border-cyan-400 text-cyan-400 hover: bg-cyan-400 hover:text-white'}`}
                >
                  {plan.name === 'Enterprise' ? 'Contact Sales' : 'Get Started'}
                  <ArrowRight className="w-8 h-8" />
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>
      {/* CTA Section */}
      <section className="py-20 px-4 sm: px-6 lg:px-8 bg-gradient-to-r from-cyan-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md: text-4xl font-bold text-white mb-6">
            Ready to Build Your First Chatbot?
          </h2>
          <p className="text-xl text-cyan-100 mb-8">
            Join thousands of businesses already using our platform to create intelligent, engaging chatbots that drive results.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/contact" 
              className="inline-flex items-center px-8 py-3 bg-white text-cyan-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors duration-300"
            >
              Start Building Today
              <ArrowRight className="w-8 h-8" />
            </Link>
            <Link 
              href="/ai-services" 
              className="inline-flex items-center px-8 py-3 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-cyan-600 transition-colors duration-300"
            >
              Explore All AI Services
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
export default AiChatbotBuilderPage