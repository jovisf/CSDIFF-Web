import styles from "./page.module.scss";
import Card from "./ui/card/Card";
import { Header } from "./ui/header/Header";
const beer = {
  name: 'English IPA, 6%',
  description: 'Пиво темне з фруктовими нотками',
  volumeLarge: '0,33',
  priceLarge: 70
}

export default function Home() {
  return (
    <div>
      <Header />
      <main className={styles.main}>
        <Card beer={beer}/>
      </main>
    </div>
  );
}
