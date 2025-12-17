import styles from './page.module.scss';
import { Header } from './ui/header/Header';

export default function Home() {
  return (
    <div>
      <Header />
      <main className={styles.main}>{'I am main'}</main>
    </div>
  );
}
