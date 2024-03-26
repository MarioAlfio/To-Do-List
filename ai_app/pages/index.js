import Head from 'next/head'
import Layout from '../components/layout';
//components/layout
import ToDoList from '../components/ai-list';

export default function Home() {
   return (
    <div>
      <Head>
        <title>To Do</title>
        <meta name="description" content="Full Stack To Do" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Layout>
        <ToDoList />
      </Layout>
    </div>
  )
} 
