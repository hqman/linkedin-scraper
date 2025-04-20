import pytest
from unittest.mock import patch, MagicMock
from src.linkedin_scraper.llm_extractor import extract_company_info
from src.linkedin_scraper.models.company import Company

# Test HTML content sample
HTML_CONTENT = """
<div class="artdeco-dropdown__content-inner">
  
          <ul>
            
<!----><!---->
          <li>
            <a tabindex="0" rel="noopener noreferrer" target="_blank" href="https://relevanceai.com" id="ember510" class="ember-view org-overflow-menu__item">
              <svg role="none" aria-hidden="true" class="org-overflow-menu__item-hue-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" data-supported-dps="24x24" data-test-icon="link-external-medium">
<!---->    
    <use href="#link-external-medium" width="24" height="24"></use>
</svg>

              Visit website
            </a>
          </li>

<!---->
<!---->
          <li>
            

    <div class="entry-point">
      
    <div></div>
  

          
              <button class="org-overflow-menu__item" type="button">
                <svg role="none" aria-hidden="true" class="org-overflow-menu__item-hue-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" data-supported-dps="24x24" data-test-icon="send-privately-medium" data-rtl="true">
<!---->    
    <use href="#send-privately-medium" width="24" height="24"></use>
</svg>

                Send in a message
              </button>
            
    </div>
  
          </li>

<!---->
<!---->
<!---->
        <li>
          <button class="org-overflow-menu__item org-top-card-overflow__report-btn" type="button">
            <svg role="none" aria-hidden="true" class="org-overflow-menu__item-hue-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" data-supported-dps="24x24" data-test-icon="report-medium">
<!---->    
    <use href="#report-medium" width="24" height="24"></use>
</svg>

            Report abuse
          </button>
        </li>

          <li>
            <a href="/company/setup/new/" id="ember511" class="ember-view org-overflow-menu__item org-top-card-overflow__create-page">
              <svg role="none" aria-hidden="true" class="org-overflow-menu__item-hue-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" data-supported-dps="24x24" data-test-icon="add-medium">
<!---->    
    <use href="#add-medium" width="24" height="24"></use>
</svg>

              Create a LinkedIn Page
            </a>
          </li>
      
          </ul>
        
</div>
<div class="org-module-card__margin-bottom">
            
    <section class="org-top-card artdeco-card">
      
    
      <div id="ember31" class="ember-view">
        
      
<!---->
        <div class="top-card-background-hero-image" style="min-height: 134px; max-height: 134px;">
          <div class="top-card-background-hero-image__bg-image">
            
    <figure class="company-hero-image-container company-hero-image-figure org-top-card__hero-image" role="button">
            
    <div class="org-cropped-image
        artdeco-card
        
         company-hero-image" id="organization-cover-single-photo-target-image">
        <div style="background-image: url(https://media.licdn.com/dms/image/v2/D563DAQHL_zCKuH4T1Q/image-scale_191_1128/image-scale_191_1128/0/1718350570656/relevanceai_cover?e=1745571600&amp;v=beta&amp;t=WD8wMGV1FwJZqHWaUG_G6puIqsoMTtl3xBfjDaXpu8k);" class="org-cropped-image__cover-image background-image">
        </div>
    </div>
  

<!---->    </figure>
  
          </div>
        </div>
        <div class="relative">
          <div class="absolute position-right mr1">
            <div class="org-top-card__badges">
<!----><!---->            </div>
          </div>
          <div>
            <div class="ph5 pb5">
              
    <div class="org-top-card__primary-content org-top-card-primary-content--zero-height-logo org-top-card__improved-primary-content--ia">
<!---->      <div class="org-top-card-primary-content__logo-container">
        <img src="https://media.licdn.com/dms/image/v2/D560BAQHYhwAvHL8aRg/company-logo_200_200/company-logo_200_200/0/1718350495354/relevanceai_logo?e=1750291200&amp;v=beta&amp;t=uwW59cctgbh2bnL72qEeUkF2qkpZu0AJkayM3fUxBiQ" loading="lazy" alt="Relevance AI logo" id="ember32" class="evi-image lazy-image ember-view org-top-card-primary-content__logo
            ">
      </div>
      <div class="block mt4">
        
    <div>
        <h1 id="ember33" class="ember-view org-top-card-summary__title
            YDIsxYHvzuGrpzZBWjsNpQHmdHPzdpKjY
            full-width
            
            " title="Relevance AI">
          Relevance AI
        </h1>
<!---->
<!---->
        <p class="org-top-card-summary__tagline">
          Built for ops teams, subject-matter experts can design powerful AI tools, AI agents and multi-agent teams without code.
        </p>

<!---->
      
    <div class="org-top-card-summary-info-list xh-highlight">
        <div class="org-top-card-summary-info-list__info-item xh-highlight">
          Software Development
        </div>

<!---->
      <div class="inline-block">
          <div class="org-top-card-summary-info-list__info-item xh-highlight">
            Surry Hills, New South Wales
          </div>

            <div class="org-top-card-summary-info-list__info-item xh-highlight">
              21K  followers
            </div>
            <a href="/search/results/people/?currentCompany=%5B%2236167121%22%5D&amp;origin=COMPANY_PAGE_CANNED_SEARCH" id="ember34" class="ember-view org-top-card-summary-info-list__info-item org-top-card-summary-info-list__info-item-link">
              <span class="t-normal t-black--light link-without-visited-state link-without-hover-state">
                  11-50 employees
              </span>
            </a>
                </div>
    </div>
  
    </div>
  
      </div>
    </div>

<!---->  

                
    <div>
<!---->
<!---->
        <div class="inline-block org-top-card-secondary-content__insights text-body-medium-bold t-black--light">
          <div class="org-top-card-secondary-content__social-proof">
              <a class="jRmKxIDSOyXycCHUdZZoTLSiiCghyNjGDU  org-top-card-secondary-content__insight link-without-visited-state t-black--light" href="http://www.linkedin.com/search/results/people/?origin=COMPANY_PAGE_CANNED_SEARCH&amp;currentCompany=%5B%2236167121%22%5D&amp;schoolFilter=%5B%222842%22%5D" data-test-app-aware-link="">
                  
    <div class="ivm-image-view-model    mr2">
        
    <div class="ivm-view-attr__img-wrapper
        
        ">
<!---->
<!---->          <img width="24" src="https://media.licdn.com/dms/image/v2/C4E03AQHZ5771co5HKA/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1519258497076?e=1750291200&amp;v=beta&amp;t=W6grvDu4f5EZJa7MEZVbnLqPNJuKfbnaujAQQCOW6Vg" loading="lazy" height="24" alt="Brian Vu" id="ember35" class="ivm-view-attr__img--centered EntityPhoto-circle-0   evi-image lazy-image ember-view">
    </div>
  
          </div>
  
                <h2 class="t-black--light link-without-visited-state text-body-small-bold">
                  <!---->Brian &amp; 1 other school alum work here<!---->
                </h2>
              </a>
<!---->          </div>
        </div>
    </div>
  

              <div class="inline-block">
<!---->
                <div>
                    
    <div class="org-top-card-primary-actions org-top-card__primary-actions">
      <div class="org-top-card-primary-actions__inner" role="region">
              
    
    <button class="follow   org-company-follow-button org-top-card-primary-actions__action artdeco-button artdeco-button--primary" aria-label="Follow" aria-pressed="false" type="button">
          <svg role="none" aria-hidden="true" class="artdeco-button__icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" data-supported-dps="16x16" data-test-icon="add-small">
<!---->    
    <use href="#add-small" width="16" height="16"></use>
</svg>

        <span aria-hidden="true">Follow</span>
    </button>
  
  

<!---->
<!---->
<!---->
<!----><!---->
              
    
    <button aria-label="Message Relevance AI" id="ember36" class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view org-top-card-primary-actions__action" data-test-message-page-button="">        <svg role="none" aria-hidden="true" class="artdeco-button__icon " xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" data-supported-dps="16x16" data-test-icon="send-privately-small" data-rtl="true">
<!---->    
    <use href="#send-privately-small" width="16" height="16"></use>
</svg>


<span class="artdeco-button__text">
    Message
</span></button>
  
<!---->  

<!---->
<!---->
<!---->      </div>

      <div id="ember37" class="ember-view"><div id="ember38" class="ember-view"><!----></div></div>
    </div>
  
                  

    <div id="ember39" class="org-top-card-overflow org-top-card__top-card-overflow">
      
    <div class="org-overflow-menu">
      <div id="ember40" class="artdeco-dropdown artdeco-dropdown--placement-bottom artdeco-dropdown--justification-left ember-view">
        <button aria-expanded="false" id="ember41" class="artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view org-overflow-menu__dropdown-trigger artdeco-button artdeco-button--1 artdeco-button--muted artdeco-button--circle artdeco-button--secondary" type="button" tabindex="0">
            <svg role="img" aria-hidden="false" aria-label="Overflow Actions" class="org-overflow-menu__trigger-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" data-supported-dps="16x16" data-test-icon="overflow-web-ios-small">
<!---->    
    <use href="#overflow-web-ios-small" width="16" height="16"></use>
</svg>

        
<!----></button>
        <div tabindex="-1" aria-hidden="true" id="ember42" class="artdeco-dropdown__content artdeco-dropdown--is-dropdown-element artdeco-dropdown__content--has-arrow artdeco-dropdown__content--arrow-right artdeco-dropdown__content--justification-left artdeco-dropdown__content--placement-bottom ember-view org-overflow-menu__content"><!----></div>
      </div>
    </div>
  

<!---->    </div>
  
                </div>
              </div>

<!---->            </div>

<!---->          </div>

<!---->
          
    
      <div id="ember43" class="ember-view">
        
      
    <nav aria-label="Organization's page navigation" class="org-page-navigation
        
        
        org-page-navigation--is-scrollable
        org-page-navigation--horizontal
        org-page-navigation--48dp org-top-card__horizontal-nav-bar artdeco-card__actions
            ">
      <ul class="org-page-navigation__items ">
        
            
  <li class="org-page-navigation__item m0
                ml1
                ">
    
              <a id="ember71" class="ember-view active pv3 ph4 t-16 t-bold t-black--light org-page-navigation__item-anchor " aria-current="page" href="/company/relevanceai/">
                Home
              </a>
            
  </li>

            
  <li class="org-page-navigation__item m0
                
                ">
    
              <a id="ember72" class="ember-view pv3 ph4 t-16 t-bold t-black--light org-page-navigation__item-anchor " aria-current="false" href="/company/relevanceai/about/">
                About
              </a>
            
  </li>

            
  <li class="org-page-navigation__item m0
                
                ">
    
              <a id="ember73" class="ember-view pv3 ph4 t-16 t-bold t-black--light org-page-navigation__item-anchor " aria-current="false" href="/company/relevanceai/posts/">
                Posts
              </a>
            
  </li>

            
  <li class="org-page-navigation__item m0
                
                ">
    
              <a id="ember74" class="ember-view pv3 ph4 t-16 t-bold t-black--light org-page-navigation__item-anchor " aria-current="false" href="/company/relevanceai/jobs/">
                Jobs
              </a>
            
  </li>

            
  <li class="org-page-navigation__item m0
                
                mr1">
    
              <a id="ember75" class="ember-view pv3 ph4 t-16 t-bold t-black--light org-page-navigation__item-anchor " aria-current="false" href="/company/relevanceai/people/">
                People
              </a>
            
  </li>

<!---->      
      </ul>
    </nav>
  
    
      </div>
  
  
        </div>
      
    
      </div>
  
  
    </section>
  
        </div>
"""


def test_company_info_extractor():
    company_info = extract_company_info(HTML_CONTENT)
    assert company_info is not None
    assert company_info["company_name"] == "Relevance AI"
    assert company_info["company_website"] == "https://relevanceai.com"
    assert (
        company_info["company_description"]
        == "Built for ops teams, subject-matter experts can design powerful AI tools, AI agents and multi-agent teams without code."
    )
    assert company_info["industry"] == "Software Development"
    assert company_info["location"] == "Surry Hills, New South Wales"
    assert company_info["followers"] == "21K"
    assert company_info["employees"] == "11-50"
