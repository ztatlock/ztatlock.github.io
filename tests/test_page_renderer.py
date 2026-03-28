from __future__ import annotations

import unittest
from pathlib import Path

from scripts.sitebuild.djot_refs import load_and_render_site_refs
from scripts.sitebuild.page_renderer import render_page_html, rewrite_local_html_targets
from scripts.sitebuild.site_config import load_site_config

ROOT = Path(__file__).resolve().parents[1]


class PageRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_site_config(ROOT)
        cls.refs_text = load_and_render_site_refs(
            people_path=cls.config.people_data_path,
            refs_path=cls.config.manual_refs_path,
        )

    def test_render_ordinary_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/about"
        html = render_page_html(
            "ordinary_page",
            "about",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            page_source_dir=self.config.page_source_dir,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)

    def test_render_publication_page_uses_explicit_canonical_url_and_aliases(self) -> None:
        canonical = "https://ztatlock.net/pubs/2024-asplos-lakeroad/"
        html = render_page_html(
            "publication_page",
            "2024-asplos-lakeroad",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            page_source_dir=self.config.page_source_dir,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
            aliases={
                "img/favicon.png": "/img/favicon.png",
                "style.css": "/style.css",
                "pubs/": "/pubs/",
                "pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf": "/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf",
            },
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn('href="/style.css"', html)
        self.assertIn('href="/pubs/"', html)
        self.assertIn(
            'href="/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf"',
            html,
        )

    def test_render_talks_index_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/talks/"
        html = render_page_html(
            "talks_index_page",
            "talks",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            talks_dir=self.config.talks_dir,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)

    def test_render_cv_index_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/cv/"
        html = render_page_html(
            "cv_index_page",
            "cv",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            cv_dir=self.config.cv_dir,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
        self.assertNotIn("__CV_STUDENTS_CURRENT_LIST__", html)
        self.assertIn("Curriculum Vitae", html)
        self.assertIn("Overview", html)
        self.assertIn("Visiting Students and Interns", html)
        self.assertIn("Ian Briggs", html)

    def test_render_service_index_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/service/"
        html = render_page_html(
            "service_index_page",
            "service",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            data_dir=self.config.data_dir,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
        self.assertNotIn("__SERVICE_REVIEWING_LIST__", html)
        self.assertIn("UW Faculty Skit Writer, Producer, and Director", html)
        self.assertIn("Hank Levy", html)
        self.assertIn("Program Committee Chair", html)
        self.assertIn("PLDI 2025", html)

    def test_render_collaborators_index_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/collaborators/"
        html = render_page_html(
            "collaborators_index_page",
            "collaborators",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            collaborators_dir=self.config.collaborators_dir,
            data_dir=self.config.data_dir,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
        self.assertNotIn("__RESEARCH_COLLABORATORS_LIST__", html)
        self.assertNotIn("__TEACHING_COLLABORATORS_LIST__", html)
        self.assertIn("James Wilcox", html)
        self.assertIn("Robert Rabe", html)

    def test_render_funding_index_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/funding/"
        html = render_page_html(
            "funding_index_page",
            "funding",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            funding_dir=self.config.funding_dir,
            data_dir=self.config.data_dir,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
        self.assertNotIn("__FUNDING_LIST__", html)
        self.assertIn("ComPort: Rigorous Testing Methods to Safeguard Software Porting", html)
        self.assertIn("NSF CCF-2017927", html)

    def test_render_news_index_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/news/"
        html = render_page_html(
            "news_index_page",
            "news",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            news_dir=self.config.news_dir,
            data_dir=self.config.data_dir,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
        self.assertNotIn("__NEWS_MONTH_GROUPS__", html)
        self.assertIn("Zachary Tatlock / News", html)
        self.assertIn("Visiting the PL and Graphics groups at Brown University", html)
        self.assertIn("Dagstuhl Seminar 26022: EGRAPHS", html)
        self.assertIn("The Neutrons project was featured", html)

    def test_render_students_index_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/students/"
        html = render_page_html(
            "students_index_page",
            "students",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            students_dir=self.config.students_dir,
            data_dir=self.config.data_dir,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
        self.assertNotIn("__STUDENTS_CURRENT_LIST__", html)
        self.assertIn("Visiting Students and Interns", html)
        self.assertIn("Zhiyuan (Kevin) Yan", html)

    def test_render_teaching_index_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/teaching/"
        html = render_page_html(
            "teaching_index_page",
            "teaching",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            data_dir=self.config.data_dir,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
        self.assertNotIn("__TEACHING_UW_COURSES_LIST__", html)
        self.assertIn("Marktoberdorf Summer School 2024", html)
        self.assertIn("Mathematician", html)
        self.assertNotIn('class="columns columns-8rem"', html)
        self.assertIn(
            '<a href="https://courses.cs.washington.edu/courses/cse505/25sp/">2025 Spring</a>\n<ul>\n<li>\nCo-Instructors: <a href="https://jamesrwilcox.com/">James Wilcox</a>',
            html,
        )
        self.assertIn("Co-Instructors: <a href=\"https://jamesrwilcox.com/\">James Wilcox</a>", html)
        self.assertIn("Tutors: <a href=\"https://jamesrwilcox.com/\">James Wilcox</a>", html)
        self.assertIn("UW CSE 599W: Systems Verification", html)
        self.assertIn("Formally verifying systems implementations", html)
        self.assertIn("Co-Instructors:", html)
        self.assertIn(">Bryan Parno</a>", html)
        self.assertIn(">Xi Wang</a>", html)
        self.assertIn("Jack Zhang", html)

    def test_render_publications_index_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/pubs/"
        html = render_page_html(
            "publications_index_page",
            "publications",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            site_url=self.config.site_url,
            webfiles_url=self.config.webfiles_url,
            publications_dir=self.config.publications_dir,
            templates_dir=self.config.templates_dir,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
        self.assertNotIn("__PUBLICATIONS_MAIN_LIST__", html)
        self.assertNotIn("__PUBLICATIONS_WORKSHOP_LIST__", html)
        self.assertIn("Target-Aware Implementation of Real Expressions", html)

    def test_rewrites_static_asset_target(self) -> None:
        html = '<link rel="stylesheet" href="style.css">'
        rewritten = rewrite_local_html_targets(
            html,
            aliases={"style.css": "/style.css"},
        )
        self.assertIn('href="/style.css"', rewritten)

    def test_rewrites_collection_index_target(self) -> None:
        html = '<a href="talks/">Talks</a>'
        rewritten = rewrite_local_html_targets(
            html,
            aliases={"talks/": "/talks/"},
        )
        self.assertIn('href="/talks/"', rewritten)

    def test_leaves_external_targets_alone(self) -> None:
        html = '<a href="https://example.com/">x</a>'
        rewritten = rewrite_local_html_targets(html, aliases={"https://example.com/": "/nope"})
        self.assertEqual(html, rewritten)
