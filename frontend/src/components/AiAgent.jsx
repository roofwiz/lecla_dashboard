import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import './AiAgent.css';

const AiAgent = () => {
    const { user } = useAuth();
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        if (isOpen && messages.length === 0 && user) {
            const welcomeMessage = {
                role: 'assistant',
                content: `Hi ${user.full_name}! I'm your Lecla ${user.role || 'Team'} Co-Pilot. How can I help you today?`
            };
            setMessages([welcomeMessage]);
        }
    }, [isOpen, user]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            // Placeholder for real API call
            const response = await fetch('http://127.0.0.1:8000/api/ai/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('lecla_token')}`
                },
                body: JSON.stringify({ message: input })
            });

            if (!response.ok) throw new Error('Failed to chat');

            const data = await response.json();
            setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
        } catch (err) {
            console.error(err);
            setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I'm having trouble connecting right now." }]);
        } finally {
            setIsLoading(false);
        }
    };

    if (!user) return null;

    return (
        <div className={`ai-agent-wrapper ${isOpen ? 'active' : ''}`}>
            <button
                className="ai-trigger"
                onClick={() => setIsOpen(!isOpen)}
                title="Lecla Co-Pilot"
            >
                {isOpen ? '✕' : '✨'}
            </button>

            {isOpen && (
                <div className="ai-chat-window">
                    <div className="ai-header">
                        <div className="ai-status">
                            <span className="pulse"></span>
                            Lecla Co-Pilot ({user.role})
                        </div>
                    </div>

                    <div className="ai-messages">
                        {messages.map((msg, i) => (
                            <div key={i} className={`message ${msg.role}`}>
                                <div className="message-content">{msg.content}</div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="message assistant loading">
                                <div className="dots"><span>.</span><span>.</span><span>.</span></div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <form className="ai-input-area" onSubmit={handleSend}>
                        <input
                            type="text"
                            placeholder="Ask me anything..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />
                        <button type="submit" disabled={isLoading}>➔</button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default AiAgent;
