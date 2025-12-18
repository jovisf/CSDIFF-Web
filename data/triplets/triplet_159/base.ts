import { Workflow, Cloud } from 'lucide-react';
export interface Service {

  id: string;
  title: string;
  description: string;
  features: string[];
  benefits: string[];
  pricing: {
    basic: string;
    pro: string;
    enterprise: string};
  contactInfo: {
  website: string;
    email: string;
    phone: string};
  price?: string;
  icon?: string;
  href: string;
  popular?: boolean;
  category: "ai" | "it" | "cloud" | "security" | "data" | "automation";
}

export const aiServices: Service[] = [
  {
    id: "ai-analytics",
    title: "AI Analytics & BI",
    description: "Transform your data into actionable insights with our advanced AI analytics platform.",
    features: [
      "Real-time data processing",
      "Predictive analytics",
      "Custom dashboards",
      "Automated reporting",
      "Machine learning models"
    ],
    benefits: [
      "Improved decision making",
      "Reduced manual analysis time",
      "Better business insights",
      "Cost savings"
    ],
    pricing: {
      basic: "$299/month",
      pro: "$999/month",
      enterprise: "Custom pricing"
    },
    contactInfo: {
      website: "https://ziontechgroup.com",
      email: "sales@ziontechgroup.com",
      phone: "+1-555-0123"
    },
    price: "Starting at $299/month",
    icon: "📊",
    href: "/services/ai-analytics",
    popular: true,
    category: "ai"
  },
  {
    id: "ai-automation",
    title: "AI Process Automation",
    description: "Automate your business processes with intelligent AI solutions that learn and adapt.",
    features: [
      "Workflow automation",
      "Document processing",
      "Customer service bots",
      "Data entry automation",
      "Smart scheduling"
    ],
    benefits: [
      "Increased efficiency",
      "Reduced human error",
      "24/7 operation",
      "Scalable solutions"
    ],
    pricing: {
      basic: "$499/month",
      pro: "$999/month",
      enterprise: "Custom pricing"
    },
    contactInfo: {
      website: "https://ziontechgroup.com",
      email: "sales@ziontechgroup.com",
      phone: "+1-555-0123"
    },
    price: "Starting at $499/month",
    icon: "🤖",
    href: "/services/ai-automation",
    popular: true,
    category: "ai"
  },
  {
    id: "ai-chatbots",
    title: "AI Chatbots & Virtual Assistants",
    description: "Deploy intelligent chatbots that provide 24/7 customer support and assistance.",
    features: [
      "Natural language processing",
      "Multi-language support",
      "Integration with CRM",
      "Voice recognition",
      "Custom training"
    ],
    benefits: [
      "24/7 customer support",
      "Reduced support costs",
      "Improved customer satisfaction",
      "Scalable support"
    ],
    pricing: {
      basic: "$199/month",
      pro: "$499/month",
      enterprise: "Custom pricing"
    },
    contactInfo: {
      website: "https://ziontechgroup.com",
      email: "sales@ziontechgroup.com",
      phone: "+1-555-0123"
    },
    price: "Starting at $199/month",
    icon: "💬",
    href: "/services/ai-chatbots",
    popular: false,
    category: "ai"
  }
]

export const itServices: Service[] = [
  {
    id: "cloud-migration",
    title: "Cloud Migration Services",
    description: "Seamlessly migrate your infrastructure to the cloud with our expert team.",
    features: [
      "AWS/Azure/GCP migration",
      "Data migration",
      "Application modernization",
      "Security compliance",
      "Performance optimization"
    ],
    benefits: [
      "Reduced infrastructure costs",
      "Improved scalability",
      "Enhanced security",
      "Better performance"
    ],
    pricing: {
      basic: "$5,000/project",
      pro: "$15,000/project",
      enterprise: "Custom pricing"
    },
    contactInfo: {
      website: "https://ziontechgroup.com",
      email: "sales@ziontechgroup.com",
      phone: "+1-555-0123"
    },
    price: "Starting at $5,000",
    icon: "☁️",
    href: "/services/cloud-migration",
    popular: true,
    category: "cloud"
  },
  {
    id: "cybersecurity",
    title: "Cybersecurity Solutions",
    description: "Protect your business with comprehensive cybersecurity services and monitoring.",
    features: [
      "Security assessment",
      "Threat monitoring",
      "Incident response",
      "Compliance auditing",
      "Security training"
    ],
    benefits: [
      "Enhanced security posture",
      "Reduced risk of breaches",
      "Compliance assurance",
      "Peace of mind"
    ],
    pricing: {
      basic: "$1,999/month",
      pro: "$4,999/month",
      enterprise: "Custom pricing"
    },
    contactInfo: {
      website: "https://ziontechgroup.com",
      email: "sales@ziontechgroup.com",
      phone: "+1-555-0123"
    },
    price: "Starting at $1,999/month",
    icon: "🔒",
    href: "/services/cybersecurity",
    popular: true,
    category: "security"
  }
]

export const allServices: Service[] = [...aiServices, ...itServices]

export default allServices