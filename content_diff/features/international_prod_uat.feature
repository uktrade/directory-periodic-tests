Feature: Find content differences between Production and UAT International environments

  Scenario Outline: Content on Productiona page "<selected>" should be the same as on respective UAT page
    When you look at the "main" section of the "<selected>" page on "International" "STAGE" and "UAT"

    Then there should be no differences

    Examples: International
      | selected                                  |
      | /                                         |
      | ?lang=de                                  |
      | ?lang=zh-hans                             |
      | industries/                               |
      | industries/engineering-and-manufacturing/ |
      | industries/healthcare-and-life-sciences/  |
