import Gallery from '../components/containers/gallery/gallery';
import Card from '../components/ui/card/Card';
import Section from '../components/ui/section/section';
import { beer } from '../static/bear';

export default function Page() {
  return (
    <main>
      <Section>
        <h2>Пиво</h2>
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
