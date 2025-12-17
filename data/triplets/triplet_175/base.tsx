'use client';
import { Zap, Brain, Users, FileText, Clock, ArrowRight, CheckCircle, Target, ShoppingCart, Calculator, Building2, Settings, Shield } from 'lucide-react';
import Link from 'next/link';
<<<<<<< HEAD
import { ArrowRight, FileText, Calculator, CheckCircle, Brain, Settings, Target, Users, Zap, Building2, ShoppingCart, Clock, Shield, Check } from 'lucide-react';;

=======
>>>>>>> origin/main
const AiInvoiceGeneratorPage: React.FC = () => {
  const features = [
    {
      icon: <Brain className="w-8 h-8 text-cyan-400" />,
      title: 'AI-Powered Generation',
      description: 'Automatically generate professional invoices using AI that understands your business patterns and client preferences.',
      benefits: ['Smart templates', 'Auto-population', 'Brand consistency', 'Learning algorithms']
    },
    {
      icon: <Calculator className="w-8 h-8 text-purple-400" />,
      title: 'Automatic Calculations',
      description: 'AI handles all calculations including taxes, discounts, and currency conversions automatically.',
      benefits: ['Tax calculations', 'Discount management', 'Multi-currency', 'Error prevention']
    },
    {
      icon: <Target className="w-8 h-8 text-green-400" />,
      title: 'Smart Categorization',
      description: 'Intelligent categorization of expenses and services for better financial tracking and reporting.',
      benefits: ['Auto-categorization', 'Expense tracking', 'Financial insights', 'Reporting']
    },
    {
      icon: <Zap className="w-8 h-8 text-orange-400" />,
      title: 'Workflow Automation',
      description: 'Streamline your invoicing process with automated workflows and follow-up reminders.',
      benefits: ['Auto-reminders', 'Payment tracking', 'Workflow automation', 'Time savings']
    }
  ];

  const useCases = [
    {
      title: 'Freelancers',
      description: 'Perfect for freelancers who need to create professional invoices quickly',
      icon: <Users className="w-6 h-6 text-blue-400" />,
      benefits: ['Quick generation', 'Professional templates', 'Time tracking', 'Client management']
    },
    {
      title: 'Small Business',
      description: 'Ideal for small businesses managing multiple clients and projects',
      icon: <Building2 className="w-6 h-6 text-green-400" />,
      benefits: ['Multi-client support', 'Project tracking', 'Team collaboration', 'Scalable pricing']
    },
    {
      title: 'Service Providers',
      description: 'Great for service-based businesses with recurring billing needs',
      icon: <Settings className="w-6 h-6 text-purple-400" />,
      benefits: ['Recurring billing', 'Service templates', 'Automated reminders', 'Payment integration']
    },
    {
      title: 'E-commerce',
      description: 'Perfect for online stores with complex product catalogs and pricing',
      icon: <ShoppingCart className="w-6 h-6 text-yellow-400" />,
      benefits: ['Product integration', 'Inventory sync', 'Bulk invoicing', 'Order management']
    }
  ];

  const pricing = [
    {
      name: 'Starter',
      price: '$19',
      period: '/month',
      description: 'Perfect for freelancers and small businesses',
      features: [
        'Up to 50 invoices/month',
        'Basic AI features',
        'Standard templates',
        'Email support',
        'PDF export'
      ],
      popular: false
    },
    {
      name: 'Professional',
      price: '$49',
      period: '/month',
      description: 'Ideal for growing businesses',
      features: [
        'Up to 500 invoices/month',
        'Advanced AI features',
        'Custom templates',
        'Priority support',
        'API access',
        'Payment integration'
      ],
      popular: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: '',
      description: 'For large organizations',
      features: [
        'Unlimited invoices',
        'Full AI suite',
        'White-label options',
        'Dedicated support',
        'Custom integrations',
        'SLA guarantee'
      ],
      popular: false
    }
  ];

  const stats = [
    { number: '95%', label: 'Time Saved', icon: <Clock className="w-6 h-6" /> },
    { number: '10K+', label: 'Invoices Generated', icon: <FileText className="w-6 h-6" /> },
    { number: '99.9%', label: 'Accuracy Rate', icon: <Target className="w-6 h-6" /> },
    { number: '24/7', label: 'Customer Support', icon: <Shield className="w-6 h-6" /> }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
            AI Invoice <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">Generator</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Create professional invoices in seconds with AI-powered automation. Streamline your billing process and get paid faster.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/contact"
              className="inline-flex items-center px-8 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-semibold rounded-lg hover:from-cyan-600 hover:to-purple-600 transition-all duration-300"
            >
              Start Free Trial
              <ArrowRight className="ml-2 w-5 h-5" />
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
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-black/20">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full mb-4">
                  {stat.icon}
                </div>
                <div className="text-3xl font-bold text-white mb-2">{stat.number}</div>
                <div className="text-gray-300">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Powerful AI Features
            </h2>
            <p className="text-lg text-gray-300 max-w-3xl mx-auto">
              Our AI invoice generator comes with everything you need to create, send, and track professional invoices efficiently.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white/5 backdrop-blur-sm rounded-2xl p-8 border border-white/10 hover:border-cyan-400/50 transition-all duration-300 group">
                <div className="mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-white mb-4">{feature.title}</h3>
                <p className="text-gray-300 mb-4">{feature.description}</p>
                <ul className="space-y-2">
                  {feature.benefits.map((benefit, idx) => (
                    <li key={idx} className="flex items-center text-sm text-gray-300">
                      <CheckCircle className="w-4 h-4 text-green-400 mr-2 flex-shrink-0" />
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-black/20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Perfect for Every Business
            </h2>
            <p className="text-lg text-gray-300 max-w-3xl mx-auto">
              Whether you&apos;re a freelancer or a large enterprise, our AI invoice generator adapts to your needs.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {useCases.map((useCase, index) => (
              <div key={index} className="bg-white/5 backdrop-blur-sm rounded-2xl p-8 border border-white/10 hover:border-purple-400/50 transition-all duration-300 group">
                <div className="mb-6">
                  {useCase.icon}
                </div>
                <h3 className="text-xl font-semibold text-white mb-4">{useCase.title}</h3>
                <p className="text-gray-300 mb-4">{useCase.description}</p>
                <ul className="space-y-2">
                  {useCase.benefits.map((benefit, idx) => (
                    <li key={idx} className="flex items-center text-sm text-gray-300">
                      <CheckCircle className="w-4 h-4 text-green-400 mr-2 flex-shrink-0" />
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
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Simple, Transparent Pricing
            </h2>
            <p className="text-lg text-gray-300 max-w-3xl mx-auto">
              Choose the plan that fits your invoicing needs. All plans include our core AI features.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {pricing.map((plan, index) => (
              <div key={index} className={`bg-white/5 backdrop-blur-sm rounded-2xl p-8 border transition-all duration-300 ${
                plan.popular 
                  ? 'border-cyan-400/50 ring-2 ring-cyan-400/20' 
                  : 'border-white/10 hover:border-cyan-400/50'
              }`}>
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
                      <CheckCircle className="w-5 h-5 text-green-400 mr-3 flex-shrink-0" />
                      <span className="text-gray-300">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Link
                  href="/contact"
                  className={`w-full inline-flex items-center justify-center px-6 py-3 font-semibold rounded-lg transition-all duration-300 ${
                    plan.popular
                      ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white hover:from-cyan-600 hover:to-purple-600'
                      : 'border-2 border-cyan-400 text-cyan-400 hover:bg-cyan-400 hover:text-white'
                  }`}
                >
                  {plan.name === 'Enterprise' ? 'Contact Sales' : 'Get Started'}
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-cyan-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Transform Your Invoicing?
          </h2>
          <p className="text-xl text-cyan-100 mb-8">
            Start your free trial today and experience the power of AI-driven invoice generation.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/contact" 
              className="inline-flex items-center px-8 py-3 bg-white text-cyan-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors duration-300"
            >
              Start Free Trial
              <ArrowRight className="ml-2 w-5 h-5" />
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
  );
};

export default AiInvoiceGeneratorPage;