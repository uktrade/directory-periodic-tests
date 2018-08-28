Feature: Every page on Production site should NOT return "X-Robots-Tag: noindex" header


    @TT-281
    @CMS-306
    @PROD
    @<service>
    Scenario Outline: Response from (PROD) "<service>" "<page>" should NOT contain "X-Robots-Tag: noindex" header
        When you visit "<page>" on "<service>" (PROD)

        Then the response should NOT contain "X-Robots-Tag: noindex" header

        Examples: PROD <service>
            | service | page                                                                                             |
            | Invest  | /                                                                                                |
            | Invest  | /contact/                                                                                        |
            | Invest  | /feedback/                                                                                       |
            | Invest  | /industries/                                                                                     |
            | Invest  | /industries/advanced-manufacturing/                                                              |
            | Invest  | /industries/aerospace/                                                                           |
            | Invest  | /industries/agri-tech/                                                                           |
            | Invest  | /industries/automotive/                                                                          |
            | Invest  | /industries/automotive/automotive-research-and-development/                                      |
            | Invest  | /industries/automotive/automotive-supply-chain/                                                  |
            | Invest  | /industries/automotive/motorsport/                                                               |
            | Invest  | /industries/capital-investment/                                                                  |
            | Invest  | /industries/chemicals/                                                                           |
            | Invest  | /industries/creative-industries/                                                                 |
            | Invest  | /industries/creative-industries/creative-content-and-production/                                 |
            | Invest  | /industries/creative-industries/digital-media/                                                   |
            | Invest  | /industries/energy/                                                                              |
            | Invest  | /industries/energy/electrical-networks/                                                          |
            | Invest  | /industries/energy/energy-waste/                                                                 |
            | Invest  | /industries/energy/nuclear-energy/                                                               |
            | Invest  | /industries/energy/offshore-wind-energy/                                                         |
            | Invest  | /industries/energy/oil-and-gas/                                                                  |
            | Invest  | /industries/financial-services/                                                                  |
            | Invest  | /industries/financial-services/asset-management/                                                 |
            | Invest  | /industries/financial-services/financial-technology/                                             |
            | Invest  | /industries/food-and-drink/                                                                      |
            | Invest  | /industries/food-and-drink/food-service-and-catering/                                            |
            | Invest  | /industries/food-and-drink/free-foods/                                                           |
            | Invest  | /industries/food-and-drink/meat-poultry-and-dairy/                                               |
            | Invest  | /industries/health-and-life-sciences/                                                            |
            | Invest  | /industries/health-and-life-sciences/medical-technology/                                         |
            | Invest  | /industries/health-and-life-sciences/pharmaceutical-manufacturing/                               |
            | Invest  | /industries/retail/                                                                              |
            | Invest  | /industries/technology/                                                                          |
            | Invest  | /industries/technology/data-analytics/                                                           |
            | Invest  | /privacy-and-cookies/                                                                            |
            | Invest  | /privacy-and-cookies/fair-processing-notice-export-opportunities/                                |
            | Invest  | /privacy-and-cookies/fair-processing-notice-export-readiness/                                    |
            | Invest  | /privacy-and-cookies/fair-processing-notice-for-smart-survey/                                    |
            | Invest  | /privacy-and-cookies/fair-processing-notice-invest-in-great-britain/                             |
            | Invest  | /privacy-and-cookies/fair-processing-notice-selling-online-overseas/                             |
            | Invest  | /privacy-and-cookies/fair-processing-notice-trade-profiles-find-a-buyer-fab-find-a-supplier-fas/ |
            | Invest  | /privacy-and-cookies/fair-processing-notice-zendesk/                                             |
            | Invest  | /terms-and-conditions/                                                                           |
            | Invest  | /uk-regions/london/                                                                              |
            | Invest  | /uk-regions/midlands/                                                                            |
            | Invest  | /uk-regions/north-england/                                                                       |
            | Invest  | /uk-regions/northern-ireland/                                                                    |
            | Invest  | /uk-regions/scotland/                                                                            |
            | Invest  | /uk-regions/south-england/                                                                       |
            | Invest  | /uk-regions/wales/                                                                               |
            | Invest  | /uk-setup-guide/                                                                                 |
            | Invest  | /uk-setup-guide/apply-uk-visa/                                                                   |
            | Invest  | /uk-setup-guide/establish-base-business-uk/                                                      |
            | Invest  | /uk-setup-guide/hire-skilled-workers-your-uk-operations/                                         |
            | Invest  | /uk-setup-guide/open-uk-business-bank-account/                                                   |
            | Invest  | /uk-setup-guide/setup-your-business-uk/                                                          |
            | Invest  | /uk-setup-guide/understand-uk-tax-and-incentives/                                                |


        Examples: PROD <service>
            | service | page                                                                  |
            | FAS     | /                                                                     |
            | FAS     | case-study/1000/an-international-profession/                          |
            | FAS     | case-study/1004/england-and-wales-a-global-legal-centre/              |
            | FAS     | case-study/1010/port-comprehensive-assessment-operations-and-manag/   |
            | FAS     | case-study/102/livingskin-for-passive-prostheses/                     |
            | FAS     | case-study/1022/spl-launches-brochure-for-the-homebrew-industry/      |
            | FAS     | case-study/23/bp/                                                     |
            | FAS     | case-study/230/poland-sees-its-first-bio-diesel-generators/           |
            | FAS     | feedback/                                                             |
            | FAS     | industries/                                                           |
            | FAS     | industries/aerospace/                                                 |
            | FAS     | industries/agritech/                                                  |
            | FAS     | industries/automotive/                                                |
            | FAS     | industries/business-and-government-partnerships/                      |
            | FAS     | industries/business-and-government-partnerships/needs                 |
            | FAS     | industries/consumer-retail/                                           |
            | FAS     | industries/contact/                                                   |
            | FAS     | industries/contact/aerospace/                                         |
            | FAS     | industries/contact/agritech/                                          |
            | FAS     | industries/contact/automotive/                                        |
            | FAS     | industries/contact/business-and-government-partnerships/              |
            | FAS     | industries/contact/consumer-retail/                                   |
            | FAS     | industries/contact/creative-services/                                 |
            | FAS     | industries/contact/cyber-security/                                    |
            | FAS     | industries/contact/education-industry/                                |
            | FAS     | industries/contact/energy/                                            |
            | FAS     | industries/contact/engineering-industry/                              |
            | FAS     | industries/contact/food-and-drink/                                    |
            | FAS     | industries/contact/healthcare/                                        |
            | FAS     | industries/contact/infrastructure/                                    |
            | FAS     | industries/contact/innovation-industry/                               |
            | FAS     | industries/contact/legal-services/                                    |
            | FAS     | industries/contact/life-sciences/                                     |
            | FAS     | industries/contact/marine/                                            |
            | FAS     | industries/contact/professional-and-financial-services/               |
            | FAS     | industries/contact/space/                                             |
            | FAS     | industries/contact/sports-economy/                                    |
            | FAS     | industries/contact/technology/                                        |
            | FAS     | industries/creative-services/                                         |
            | FAS     | industries/cyber-security/                                            |
            | FAS     | industries/education-industry/                                        |
            | FAS     | industries/energy/                                                    |
            | FAS     | industries/engineering-industry/                                      |
            | FAS     | industries/food-and-drink/                                            |
            | FAS     | industries/healthcare/                                                |
            | FAS     | industries/infrastructure/                                            |
            | FAS     | industries/innovation-industry/                                       |
            | FAS     | industries/legal-services/                                            |
            | FAS     | industries/life-sciences/                                             |
            | FAS     | industries/marine/                                                    |
            | FAS     | industries/professional-and-financial-services/                       |
            | FAS     | industries/space/                                                     |
            | FAS     | industries/sports-economy/                                            |
            | FAS     | industries/technology/                                                |
            | FAS     | industry-articles/UK-agritech-strengths-article/                      |
            | FAS     | industry-articles/a-focus-on-regulatory-technology-solutions-article/ |
            | FAS     | industry-articles/a-global-centre-for-life-sciences/                  |
            | FAS     | industry-articles/building-fintech-bridges-article/                   |
            | FAS     | industry-articles/established-mining-industry-article/                |
            | FAS     | industry-articles/global-humanitarian-support-article/                |
            | FAS     | industry-articles/global-rail-experience-article/                     |
            | FAS     | industry-articles/helping-you-buy-from-the-uk-article-ukef/           |
            | FAS     | industry-articles/highly-rated-primary-care/                          |
            | FAS     | industry-articles/home-of-oil-and-gas-innovation-article/             |
            | FAS     | industry-articles/how-education-is-going-digital/                     |
            | FAS     | industry-articles/how-tech-is-changing-the-way-we-bank-article/       |
            | FAS     | industry-articles/innovative-airport-solutions-article/               |
            | FAS     | industry-articles/leading-the-world-in-cancer-care/                   |
            | FAS     | industry-articles/life-changing-artificial-intelligence-AI/           |
            | FAS     | industry-articles/the-changing-face-of-visual-effects/                |
            | FAS     | industry-articles/trusted-construction-partners-article/              |
            | FAS     | industry-articles/uk-centres-of-excellence/                           |
            | FAS     | industry-articles/uk-cyber-security-hubs/                             |
            | FAS     | industry-articles/world-class-research-centre-article/                |
            | FAS     | suppliers/00392279/contact/                                           |
            | FAS     | suppliers/00392279/gl-events-uk-limited/                              |


        Examples: PROD <service>
            | service | page                                                                  |
            | ExRead  | /                                                                     |
            | ExRead  | about/                                                                |
            | ExRead  | business-planning/                                                    |
            | ExRead  | customer-insight/                                                     |
            | ExRead  | export-opportunities/                                                 |
            | ExRead  | finance/                                                              |
            | ExRead  | get-finance/                                                          |
            | ExRead  | getting-paid/                                                         |
            | ExRead  | international/                                                        |
            | ExRead  | international/privacy-and-cookies/                                    |
            | ExRead  | international/terms-and-conditions/                                   |
            | ExRead  | market-research/                                                      |
            | ExRead  | new/                                                                  |
            | ExRead  | occasional/                                                           |
            | ExRead  | operations-and-compliance/                                            |
            | ExRead  | performance-dashboard/                                                |
            | ExRead  | privacy-and-cookies/                                                  |
            | ExRead  | regular/                                                              |
            | ExRead  | story/hello-babys-rapid-online-growth/                                |
            | ExRead  | story/online-marketplaces-propel-freestyle-xtreme-sales/              |
            | ExRead  | story/york-bag-retailer-goes-global-via-e-commerce/                   |
            | ExRead  | terms-and-conditions/                                                 |
            | ExRead  | triage/                                                               |
            | ExRead  | triage/exported-before/                                               |


        Examples: PROD <service>
            | service | page                     |
            | SSO     | /                        |
            | SSO     | accounts/login/          |
            | SSO     | accounts/password/reset/ |
            | SSO     | accounts/signup/         |


        Examples: PROD <service>
            | service | page                     |
            | Profile | /                        |
            | Profile | about/          |


        Examples: PROD <service>
            | service    | page                         |
            | Contact-Us | /                            |
            | Contact-Us | directory/FeedbackForm/      |
            | Contact-Us | whatever/FeedbackForm/       |
            | Contact-Us | whatever/FeedbackForm/thanks |
            | Contact-Us | soo/TriageForm/              |
            | Contact-Us | soo/TriageForm/thanks        |
            | Contact-Us | ping/                        |
            | Contact-Us | companies/                   |


        Examples: PROD <service>
            | service | page                                            |
            | ExOpps  | /                                               |
            | ExOpps  | opportunities/                                  |
            | ExOpps  | opportunities?sectors[]=creative-media          |
            | ExOpps  | opportunities?sectors[]=education-training      |
            | ExOpps  | opportunities/framework-agreement-meat-and-fish |


        Examples: PROD <service>
            | service | page                                                                          |
            | SOO     | /                                                                             |
            | SOO     | markets/shortlist/                                                            |
            | SOO     | markets/story/chiswick-retailer-strikes-deal-with-amazon-australia/           |
            | SOO     | markets/story/global-marketplaces-drive-burlingham-london-to-success/         |
            | SOO     | markets/story/red-herring-games-take-their-mysteries-overseas-through-amazon/ |
