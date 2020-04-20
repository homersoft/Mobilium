//
//  UITextField+horizontalContentHuggingPriority.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Grzegorz Przybyła. All rights reserved.
//

import UIKit

extension UITextField {
    var horizontalContentHuggingPriority: UILayoutPriority {
        get { contentHuggingPriority(for: .horizontal) }
        set { setContentHuggingPriority(newValue, for: .horizontal) }
    }
}
