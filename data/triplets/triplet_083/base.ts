export interface StructuredData {
  '@context': string;
  '@type': string;
  name: string;
  description: string;
  url: string;
  logo?: string;
  sameAs?: string[];
}

export interface SEOData {
  title: string;
  description: string;
  keywords: string[];
  canonical?: string;
  ogTitle?: string;
  ogDescription?: string;
  ogImage?: string;
  ogUrl?: string;
  twitterCard?: string;
  twitterTitle?: string;
  twitterDescription?: string;
  twitterImage?: string;
  structuredData?: StructuredData;
}

export const defaultSEOData: SEOData = {
  title: 'Zion Tech Group - AI & Technology Solutions',
  description: 'Leading provider of AI-powered solutions, 5G technology, and innovative software development services.',
  keywords: ['AI', 'Artificial Intelligence', '5G', 'Technology', 'Software Development', 'Machine Learning'],
  canonical: 'https://ziontechgroup.com',
  ogTitle: 'Zion Tech Group - AI & Technology Solutions',
  ogDescription: 'Leading provider of AI-powered solutions, 5G technology, and innovative software development services.',
  ogImage: 'https://ziontechgroup.com/og-image.jpg',
  ogUrl: 'https://ziontechgroup.com',
  twitterCard: 'summary_large_image',
  twitterTitle: 'Zion Tech Group - AI & Technology Solutions',
  twitterDescription: 'Leading provider of AI-powered solutions, 5G technology, and innovative software development services.',
  twitterImage: 'https://ziontechgroup.com/twitter-image.jpg',
  structuredData: {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Zion Tech Group',
    description: 'Leading provider of AI-powered solutions, 5G technology, and innovative software development services.',
    url: 'https://ziontechgroup.com',
    logo: 'https://ziontechgroup.com/logo.png',
    sameAs: [
      'https://linkedin.com/company/ziontechgroup',
      'https://twitter.com/ziontechgroup',
      'https://github.com/ziontechgroup'
    ]
  }
};

export const generatePageSEO = (pageData: Partial<SEOData>): SEOData => {
  return {
    ...defaultSEOData,
    ...pageData,
    keywords: [...defaultSEOData.keywords, ...(pageData.keywords || [])]
  };
};

export const generateStructuredData = (data: Partial<StructuredData>): StructuredData => {
  return {
    ...defaultSEOData.structuredData!,
    ...data
  };
};