"use client";

import Image from "next/image";
import { useEffect, useMemo, useState } from "react";

type GalleryItem = {
  id: string;
  title: string;
  takenAt: string;
  tags: string[];
  src: string;
};

const ITEMS: GalleryItem[] = [
  {
    id: "a1",
    title: "Calico Stretch",
    takenAt: "2026-02-16",
    tags: ["calico", "indoor", "lounging"],
    src: "/cat-1.jpg",
  },
  {
    id: "a2",
    title: "Nap Paws",
    takenAt: "2026-02-11",
    tags: ["kitten", "sleeping", "closeup"],
    src: "/cat-2.jpg",
  },
  {
    id: "a3",
    title: "Sofa Peek",
    takenAt: "2026-02-07",
    tags: ["kitten", "playful", "indoor"],
    src: "/cat-3.jpg",
  },
  {
    id: "a4",
    title: "Blanket Portrait",
    takenAt: "2026-02-03",
    tags: ["ginger", "portrait", "closeup"],
    src: "/cat-4.jpg",
  },
  {
    id: "a5",
    title: "Garden Litter",
    takenAt: "2026-01-29",
    tags: ["kittens", "outdoor", "grass"],
    src: "/cat-5.jpg",
  },
  {
    id: "a6",
    title: "Blue-Eyed Roll",
    takenAt: "2026-01-22",
    tags: ["white-cat", "sunlight", "floor"],
    src: "/cat-6.jpg",
  }
];

const TAGS = ["all", ...Array.from(new Set(ITEMS.flatMap((x) => x.tags)))];

type SortKey = "newest" | "title";

export default function Home() {
  const [query, setQuery] = useState("");
  const [tag, setTag] = useState<(typeof TAGS)[number]>("all");
  const [sort, setSort] = useState<SortKey>("newest");
  const [selected, setSelected] = useState<GalleryItem | null>(null);
  const [favorites, setFavorites] = useState<Set<string>>(() => {
    if (typeof window === "undefined") return new Set();
    try {
      const raw = localStorage.getItem("gallery:favorites");
      if (!raw) return new Set();
      const ids = JSON.parse(raw) as unknown;
      if (!Array.isArray(ids)) return new Set();
      return new Set(ids.filter((x) => typeof x === "string"));
    } catch {
      return new Set();
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem("gallery:favorites", JSON.stringify(Array.from(favorites)));
    } catch {
      // ignore
    }
  }, [favorites]);

  useEffect(() => {
    if (!selected) return;
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") setSelected(null);
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [selected]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    let list = ITEMS.filter((x) => (tag === "all" ? true : x.tags.includes(tag)));
    if (q) {
      list = list.filter((x) => {
        const hay = `${x.title} ${x.tags.join(" ")} ${x.takenAt}`.toLowerCase();
        return hay.includes(q);
      });
    }
    list = [...list].sort((a, b) => {
      if (sort === "title") return a.title.localeCompare(b.title);
      return b.takenAt.localeCompare(a.takenAt);
    });
    return list;
  }, [query, tag, sort]);


  return (
    <main className="container">
      <section className="card" style={{ padding: 18 }}>
        <div className="header">
          <div>
            <h1 className="title">Gallery</h1>
          </div>
          <div className="badge" aria-label="items summary">
            {filtered.length} / {ITEMS.length}
          </div>
        </div>

        <div className="toolbar">
          <div className="search" role="search">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                d="M10.5 18.5a8 8 0 1 1 0-16 8 8 0 0 1 0 16Z"
                stroke="rgba(2,6,23,0.55)"
                strokeWidth="1.6"
              />
              <path
                d="M16.5 16.5 21 21"
                stroke="rgba(2,6,23,0.55)"
                strokeWidth="1.6"
                strokeLinecap="round"
              />
            </svg>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search (title/tags/date)…"
              aria-label="search"
            />
          </div>

          <select
            className="select"
            value={sort}
            onChange={(e) => setSort(e.target.value as SortKey)}
            aria-label="sort"
          >
            <option value="newest">Newest</option>
            <option value="title">Title</option>
          </select>
        </div>

        <div className="pills" aria-label="tag filters">
          {TAGS.map((t) => (
            <button
              key={t}
              className={`pill ${tag === t ? "pillActive" : ""}`}
              onClick={() => setTag(t)}
              type="button"
            >
              {t === "all" ? "All" : t}
            </button>
          ))}
        </div>

        {filtered.length === 0 ? (
          <div className="empty card">
            No results. Try a different query or tag.
          </div>
        ) : (
          <div className="grid" aria-label="gallery grid">
            {filtered.map((item) => {
              const isFav = favorites.has(item.id);
              return (
                <button
                  key={item.id}
                  className="card tile"
                  onClick={() => setSelected(item)}
                  type="button"
                  aria-label={`open ${item.title}`}
                >
                  <div className="thumb">
                    <Image
                      src={item.src}
                      alt={item.title}
                      fill
                      sizes="(max-width: 560px) 100vw, (max-width: 900px) 50vw, 33vw"
                    />
                  </div>
                  <div className="tileMeta">
                    <h3 className="tileTitle">{item.title}</h3>
                    <span className="badge">{isFav ? "★" : item.takenAt}</span>
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </section>

      {selected && (
        <div
          className="overlay"
          role="dialog"
          aria-modal="true"
          aria-label="preview modal"
          onMouseDown={(e) => {
            if (e.target === e.currentTarget) setSelected(null);
          }}
        >
          <div className="modal">
            <div className="modalBody">
              <div className="modalMedia">
                <div className="thumb">
                  <Image
                    src={selected.src}
                    alt={selected.title}
                    fill
                    sizes="(max-width: 820px) 100vw, 60vw"
                  />
                </div>
              </div>
              <div className="modalInfo">
                <div className="modalHeader">
                  <div>
                    <h2 className="modalTitle">{selected.title}</h2>
                    <div className="pills" style={{ margin: "10px 0 0", gap: 6 }}>
                      <span className="badge">{selected.takenAt}</span>
                      {selected.tags.map((t) => (
                        <button
                          key={t}
                          className="pill"
                          type="button"
                          onClick={() => {
                            setTag(t);
                            setSelected(null);
                          }}
                          aria-label={`filter tag ${t}`}
                        >
                          {t}
                        </button>
                      ))}
                    </div>
                  </div>
                  <button className="closeX" type="button" onClick={() => setSelected(null)} aria-label="close">
                    ✕
                  </button>
                </div>

                <div className="modalActions">
                  <button
                    className={`btn ${favorites.has(selected.id) ? "btnPrimary" : ""}`}
                    type="button"
                    onClick={() => {
                      setFavorites((prev) => {
                        const next = new Set(prev);
                        if (next.has(selected.id)) next.delete(selected.id);
                        else next.add(selected.id);
                        return next;
                      });
                    }}
                  >
                    {favorites.has(selected.id) ? "Remove favorite" : "Add to favorites"}
                  </button>
                  <button
                    className="btn"
                    type="button"
                    onClick={() => {
                      navigator.clipboard?.writeText(selected.title).catch(() => {});
                    }}
                  >
                    Copy title
                  </button>
                  <button className="btn" type="button" onClick={() => setSelected(null)}>
                    Close (ESC)
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
