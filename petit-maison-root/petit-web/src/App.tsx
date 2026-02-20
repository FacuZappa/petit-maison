import { useState } from 'react';
import { Navbar } from './components/layout/Navbar';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <Navbar />
      <main className="main-content">
      </main>
    </>
  );
}

export default App