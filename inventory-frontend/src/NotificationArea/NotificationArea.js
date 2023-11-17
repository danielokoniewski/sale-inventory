import React, { useState, forwardRef, useImperativeHandle, useEffect } from 'react';
import './NotificationArea.style.css';

export const showNotification = (message, style, notificationRef) => {
    /* uses a reference to show the notification */
    if (notificationRef && notificationRef.current) {
        notificationRef.current.showNotification({
            newMessage: message,
            newStyle: style,
        });
    } else {
        switch (style) {
            case 'error':
                console.error(message)
                break;
            default:
                console.info(message)
        }
    }
};


const NotificationArea = forwardRef(({ style: initialStyle }, ref) => {
    const [notifications, setNotifications] = useState([]);

    const getClassName = ((style) => {
        switch (style) {
            case 'error':
                return 'error';
            case 'ok':
                return 'ok';
            case 'info':
                return 'info';
            default:
                return 'info';
        }
    });

    const Notification = ({ message, style }) => (
        <div className={`notification ${getClassName(style)}`} onClick={() => hideNotification(message)}>
            {message.split("\n").map((x, index) => <div key={index}>{x}</div>)}
        </div>
    );

    const hideNotification = (message) => {
        setNotifications((prevNotifications) => prevNotifications.filter((notification) => notification.message !== message));
    };

    const showNotification = ({ newMessage, newStyle }) => {
        setNotifications((prevNotifications) => [...prevNotifications, { message: newMessage, style: newStyle }]);
    };

    useEffect(() => {
        // Use effect to automatically remove notifications after 2 seconds
        const timeoutIds = notifications.map((notification, index) =>
            setTimeout(() => {
                hideNotification(notification.message);
            }, 2000 + index * 100) // Stagger the timeouts for a nicer effect
        );

        // Clear the timeouts when the component is unmounted
        return () => timeoutIds.forEach((timeoutId) => clearTimeout(timeoutId));
    }, [notifications]);

    useImperativeHandle(ref, () => ({
        showNotification,
    }));

    return (
        <div>
            {notifications.map((notification, index) => (
                <Notification key={index} message={notification.message} style={notification.style} />
            ))}
        </div>
    );
});

export default NotificationArea;