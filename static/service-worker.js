self.addEventListener("install", e => {
    e.waitUntil(
        caches.open("hotel-client").then(cache => {
            return cache.addAll([
                "/static/client.html"
            ]);
        })
    );
});
