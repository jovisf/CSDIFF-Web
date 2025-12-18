"use client";
import Gallery from "../components/containers/gallery/gallery";
import Card from "../components/ui/card/Card";
import Section from "../components/ui/section/section";
import { beer } from "../static/bear";
import Filters from "../components/containers/filters/Filters";
import "./shop.scss";

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
            .map((el, idx) => (
              <Card {...beer} key={idx} />
            ))}
        </Gallery>
      </Section>
    </main>
  );
}
