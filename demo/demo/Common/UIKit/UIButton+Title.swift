//
//  UIButton.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import UIKit

extension UIButton {
    var title: String? {
        get { titleLabel?.text }
        set { setTitle(newValue, for: .normal) }
    }
    var titleColor: UIColor? {
        get { titleLabel?.tintColor }
        set { setTitleColor(newValue, for: .normal) }
    }
}
