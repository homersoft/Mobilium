//
//  ModuleFactory.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import UIKit

class ModuleFactory {
    func makeLoginVC(coordinator: LoginViewCoordinator) -> UIViewController {
        let viewModel = LoginViewModel(coordinator: coordinator)
        return LoginViewController(viewModel: viewModel)
    }

    func makeAccountVC(for user: User, coordinator: AccountCoordinator) -> UIViewController {
        let viewModel = AccountViewModel(currentUser: user, coordinator: coordinator)
        return AccountViewController(viewModel: viewModel)
    }
}
