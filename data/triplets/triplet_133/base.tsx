<<<<<<< HEAD
=======

>>>>>>> origin/main
import { Metadata} from 'next';
import Navigation from '../components/Navigation';
import Footer from '../components/Footer';

export const metadata: Metadata = {
  title: 'Page - Zion Tech Group',
  description: 'Professional page services by Zion Tech Group.',
  keywords: 'page, services, technology, AI, IT solutions'
};

const PagePage = () => {
  return (
    <div className="min-h-screen bg-white">
      <Navigation />
      
      <section className="pt-20 pb-16 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Page
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Professional page services by Zion Tech Group.
          </p>
          <div className="space-y-4">
            <p className="text-gray-400">
              Our page solutions are designed to help your business grow and succeed.
            </p>
            <p className="text-gray-400">
              Contact us to learn more about how we can help you achieve your goals.
            </p>
          </div>
                </div>
      </section>

      <Footer />
    </div>
  );
};

export default PagePage;
