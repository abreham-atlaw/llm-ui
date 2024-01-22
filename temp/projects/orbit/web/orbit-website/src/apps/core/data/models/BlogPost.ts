// src/apps/core/data/models/BlogPost.ts
export default class BlogPost {
    title: string;
    content: string;
    author: string;
    date: Date;

    constructor({
        title,
        content,
        author,
        date,
    }: {
        title: string;
        content: string;
        author: string;
        date: Date;
    }) {
        this.title = title;
        this.content = content;
        this.author = author;
        this.date = date;
    }
}

