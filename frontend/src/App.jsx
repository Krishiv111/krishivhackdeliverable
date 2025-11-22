import "./App.css";
import { useEffect, useState } from "react";
import Quote from "./Quote";

function App() {
    const [quotes, setQuotes] = useState([]);

   
    const loadQuotes = () => {
        fetch("/api/quotes")
            .then((res) => res.json())
            .then((data) => setQuotes(data))
            .catch((err) => console.error("Error fetching quotes:", err));
    };

   
    useEffect(() => {
        loadQuotes();
    }, []);

   
    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);

        await fetch("/api/quote", {
            method: "POST",
            body: formData,
        });

        e.target.reset();
        loadQuotes(); 
    };

    return (
        <div className="App">
            <h1>Hack at UCI Tech Deliverable</h1>

            <h2>Submit a quote</h2>
            <form onSubmit={handleSubmit}>
                <label>Name</label>
                <input type="text" name="name" required />

                <label>Quote</label>
                <input type="text" name="message" required />

                <button type="submit">Submit</button>
            </form>

            <h2>Previous Quotes</h2>
            <div className="messages">
                {quotes.map((q, index) => (
                    <Quote
                        key={index}
                        name={q.name}
                        message={q.message}
                        time={q.time}
                    />
                ))}
            </div>
        </div>
    );
}

export default App;
