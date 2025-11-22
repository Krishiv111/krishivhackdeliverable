export default function Quote({ name, message, time }) {
    return (
        <div className="quote">
            <h3>{name}</h3>
            <p>{message}</p>
            <small>{new Date(time).toLocaleString()}</small>
        </div>
    );
}
// use this file to render each code so the App.jsx isn't overkill