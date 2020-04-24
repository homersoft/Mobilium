//
//  ModuleFactory.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import UIKit

class ModuleFactory {
    func makeLoginVC() -> UIViewController {
        return LoginViewController()
    }

    func makeAccountVC() -> UIViewController {
        return AccountViewController()
    }
}
