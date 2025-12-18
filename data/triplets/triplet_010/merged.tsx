'use client';
import Filters from '../components/containers/filters/Filters';
import Gallery from '../components/containers/gallery/gallery';
import Card from '../components/ui/card/Card';
import Section from '../components/ui/section/section';
import { beer } from '../static/bear';
import './shop.scss';

export default function Page() {
  return (
    <main className="shop-page">
      <Section>
        <h1>
          <span className="t-b-100">Khmilna Oaza</span> | Магазин
        </h1>
        <Filters />
        <Gallery>
          {Array(12)
            .fill(1)
            .map(() => (
              <Card {...beer} key={beer.id} />
            ))}
        </Gallery>
      </Section>
    </main>
  );
}
